import logging, random, stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from iprovider.models import Payment, CurrencyRate, Country

logger = logging.getLogger(__name__)

@login_required
def create_payment(request):
    countries = Country.objects.all().order_by('name')
    currencies = CurrencyRate.objects.values_list('currency', flat=True)
    if not currencies:
        default_currencies = [
            {'currency': 'USD', 'rate': 1.0},
            {'currency': 'EUR', 'rate': 1.08},
            {'currency': 'RUB', 'rate': 0.011},
        ]
        for curr in default_currencies:
            CurrencyRate.objects.get_or_create(
                currency=curr['currency'],
                defaults={'rate_to_usd': curr['rate']}
            )
        currencies = CurrencyRate.objects.values_list('currency', flat=True)

    return render(request, 'iprovider/profile/deposit.html', {
        'countries': countries,
        'currencies': currencies,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
def create_checkout_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    amount_str = request.POST.get('amount')
    currency = request.POST.get('currency', 'USD').upper()

    try:
        amount = float(amount_str)
        if amount <= 0:
            return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    if not CurrencyRate.objects.filter(currency=currency).exists():
        return JsonResponse({'error': f'Currency {currency} not supported'}, status=400)

    unit_amount = int(amount * 100)
    try:
        request.session['pending_stripe'] = {
            'amount': amount,
            'currency': currency,
            'user_id': request.user.id,
        }
        request.session.modified = True

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Balance replenishment ({currency} {amount})',
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/'),
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
            metadata={
                'amount': str(amount),
                'currency': currency,
                'user_id': str(request.user.id),
            }
        )
        return JsonResponse({'sessionId': session.id})
    except Exception as e:
        logger.error(f"Stripe session creation error: {e}")
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def payment_success(request):
    pending = request.session.get('pending_stripe')
    if not pending:
        messages.error(request, _('Payment session expired. Please try again.'))
        return redirect('create_payment')

    amount = pending['amount']
    currency = pending['currency']
    user = request.user

    if currency == 'USD':
        amount_usd = amount
    else:
        try:
            rate = CurrencyRate.objects.get(currency=currency)
            amount_usd = amount * float(rate.rate_to_usd)
        except CurrencyRate.DoesNotExist:
            messages.error(request, _(f'Currency {currency} not supported.'))
            del request.session['pending_stripe']
            return redirect('create_payment')

    Payment.objects.create(
        user=user,
        amount=amount,
        currency=currency,
        transaction_type=Payment.TransactionType.DEPOSIT,
        status=Payment.Status.SUCCEEDED,
        payment_method='stripe',
        transaction_id=f"stripe_{user.id}_{random.randint(1000, 9999)}",
        payment_data={'stripe': True}
    )

    profile = user.profile
    profile.balance += amount_usd
    profile.save()

    del request.session['pending_stripe']
    messages.success(request, _(f'Balance topped up with {amount} {currency}.'))
    return redirect('profile')

@login_required
def payment_cancel(request):
    if 'pending_stripe' in request.session:
        del request.session['pending_stripe']
    messages.info(request, _('Payment cancelled. You can try again.'))
    return redirect('create_payment')
