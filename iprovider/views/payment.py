import logging
import random
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
    """
    Двухшаговая имитация платежа с генерацией кода в консоль Django.
    Шаг 1: инициирование (POST с action=initiate) – генерирует код, сохраняет в сессии.
    Шаг 2: подтверждение (POST с action=confirm) – проверяет код, зачисляет баланс.
    GET: показывает форму оплаты с выбором страны и валюты.
    """
    if request.method == 'POST':
        action = request.POST.get('action')

        # --- Шаг 1: инициирование платежа ---
        if action == 'initiate':
            amount = request.POST.get('amount')
            currency = request.POST.get('currency', 'USD').upper()
            card_number = request.POST.get('card_number', '').replace(' ', '')
            card_expiry = request.POST.get('card_expiry', '')
            card_cvv = request.POST.get('card_cvv', '')

            # Базовая проверка
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    return JsonResponse({'error': _('Amount must be greater than zero.')}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'error': _('Invalid amount.')}, status=400)

            if len(card_number) < 15:
                return JsonResponse({'error': _('Invalid card number.')}, status=400)

            # Проверка, что валюта существует в курсах
            try:
                CurrencyRate.objects.get(currency=currency)
            except CurrencyRate.DoesNotExist:
                return JsonResponse({'error': _(f'Currency {currency} is not supported.')}, status=400)

            # Генерация 6-значного кода
            otp_code = f"{random.randint(0, 999999):06d}"

            # Сохраняем в сессии
            request.session['pending_payment'] = {
                'amount': amount_float,
                'currency': currency,
                'otp_code': otp_code,
                'user_id': request.user.id,
            }
            request.session.modified = True

            # Выводим код в консоль Django (терминал)
            print(f"\n🔐 [3DS CODE for user {request.user.username}]: {otp_code}\n")
            logger.info(f"3DS code for user {request.user.id}: {otp_code}")

            return JsonResponse({'status': 'otp_required'})

        # --- Шаг 2: подтверждение платежа ---
        elif action == 'confirm':
            otp_input = request.POST.get('otp_code', '')
            pending = request.session.get('pending_payment')

            if not pending:
                messages.error(request, _('Payment session expired. Please start over.'))
                return redirect('create_payment')

            # Проверка кода
            if otp_input != pending['otp_code']:
                messages.error(request, _('Invalid verification code.'))
                return redirect('create_payment')

            amount_float = pending['amount']
            currency = pending['currency']

            # Конвертация в USD для баланса
            if currency == 'USD':
                amount_usd = amount_float
            else:
                try:
                    rate_obj = CurrencyRate.objects.get(currency=currency)
                    amount_usd = amount_float * float(rate_obj.rate_to_usd)
                except CurrencyRate.DoesNotExist:
                    messages.error(request, _(f'Currency {currency} not supported.'))
                    if 'pending_payment' in request.session:
                        del request.session['pending_payment']
                    return redirect('create_payment')

            # Создаём запись платежа (оригинальная сумма и валюта)
            Payment.objects.create(
                user=request.user,
                amount=amount_float,
                currency=currency,
                transaction_type=Payment.TransactionType.DEPOSIT,
                status=Payment.Status.SUCCEEDED,
                payment_method='mock',
                transaction_id=f"mock_{request.user.id}_{amount_float}_{currency}_{random.randint(1000, 9999)}",
                payment_data={'mock': True}
            )

            # Пополняем баланс (в USD)
            profile = request.user.profile
            profile.balance += amount_usd
            profile.save()

            # Очищаем сессию
            if 'pending_payment' in request.session:
                del request.session['pending_payment']

            messages.success(request,
                             _(f'Balance topped up with {amount_float} {currency} (MOCK MODE). Converted to ${amount_usd:.2f} USD.'))
            return redirect('profile')

        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    # --- GET-запрос: отображаем форму ---
    countries = Country.objects.all().order_by('name')

    # Список доступных валют из таблицы курсов
    currencies = CurrencyRate.objects.values_list('currency', flat=True)
    if not currencies:
        # Если курсов нет, создаём дефолтные
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
        'mock_payments': getattr(settings, 'MOCK_PAYMENTS', True),
    })