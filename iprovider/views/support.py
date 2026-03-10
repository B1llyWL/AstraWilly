from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from iprovider.models import FAQ, Country, City
from iprovider.forms import SupportTicketForm
from iprovider.tasks import send_support_ticket_email

def support(request):
    """Страница поддержки с формой обратной связи и FAQ"""
    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')

    selected_country = None
    selected_city = None

    if selected_country_id:
        try:
            selected_country = Country.objects.get(id=selected_country_id)
        except Country.DoesNotExist:
            pass

    if selected_city_id:
        try:
            selected_city = City.objects.get(id=selected_city_id)
        except City.DoesNotExist:
            pass

    faqs = FAQ.objects.filter(is_active=True)

    if request.method == 'POST':
        form = SupportTicketForm(request.POST, user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            ticket = form.save(commit=False)
            if request.user.is_authenticated:
                ticket.user = request.user
            ticket.save()

            # Асинхронная отправка email через Celery
            send_support_ticket_email.delay(
                ticket.id,
                ticket.name,
                ticket.email,
                ticket.subject,
                ticket.message
            )

            messages.success(request, _('Your message has been sent. We will contact you soon.'))
            return redirect('support')
    else:
        form = SupportTicketForm(user=request.user if request.user.is_authenticated else None)

    context = {
        'title': 'AstraWilly - Support',
        'company_name': 'AstraWilly',
        'selected_country': selected_country,
        'selected_city': selected_city,
        'countries': Country.objects.all(),
        'faqs': faqs,
        'form': form,
    }
    return render(request, 'iprovider/support.html', context)