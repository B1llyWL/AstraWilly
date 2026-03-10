"""Заявки, подключения, отмены"""
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
import logging
import sys

from iprovider.models import (
    Tariff, Separately, Packets, Vacancy, Country, City,
    Subscription, Payment, ConnectionRequest,
)

logger = logging.getLogger(__name__)


@login_required
def create_connection_request(request, item_type, item_id):
    """Создание заявки на подключение тарифа/услуги/вакансии"""
    # Отладка: вывод в консоль сервера
    print(f"CALLED: create_connection_request with item_type={item_type}, item_id={item_id}", file=sys.stderr)
    logger.debug(f"Creating request: {item_type} id={item_id} for user {request.user.id}")

    # Определяем объект по типу
    model_map = {
        'tariff': Tariff,
        'separately': Separately,
        'packet': Packets,
        'vacancy': Vacancy,
    }
    model = model_map.get(item_type)
    if not model:
        messages.error(request, _('Invalid item type'))
        return redirect('home')

    try:
        item = get_object_or_404(model, id=item_id)
    except Exception as e:
        logger.error(f"Error getting object: {e}")
        messages.error(request, _('Object not found.'))
        return redirect('home')

    # Проверяем, нет ли уже активной заявки
    existing = ConnectionRequest.objects.filter(
        user=request.user,
        status__in=['pending', 'in_progress', 'approved'],
        **{item_type: item}
    ).first()

    if existing:
        messages.info(request, _('You already have an active request for this item.'))
        return redirect('profile')

    try:
        # Создаем заявку
        conn_req = ConnectionRequest.objects.create(
            user=request.user,
            **{item_type: item},
            status='pending',
        )
        # Отладка: проверяем, что ID созданного объекта и связанное поле заполнены
        related_field_id = getattr(conn_req, f'{item_type}_id')
        print(f"Created request id={conn_req.id}, {item_type}_id={related_field_id}", file=sys.stderr)
        logger.debug(f"Created request id={conn_req.id}, {item_type}_id={related_field_id}")

        messages.success(request, _('Request sent! A manager will contact you soon.'))
    except Exception as e:
        logger.error(f"Error creating request: {e}")
        print(f"ERROR: {e}", file=sys.stderr)
        messages.error(request, _('Error creating request. Please try again.'))

    return redirect('profile')

@login_required
def quick_connect(request, item_type, item_id):
    """Быстрая заявка с автозаполнением контактов"""
    model_map = {
        'tariff': Tariff,
        'separately': Separately,
        'packet': Packets,
        'vacancy': Vacancy,
    }
    model = model_map.get(item_type)
    if not model:
        messages.error(request, _('Invalid item type'))
        return redirect('home')

    item = get_object_or_404(model, id=item_id)

    # Проверка на дубликаты
    existing = ConnectionRequest.objects.filter(
        user=request.user,
        status__in=['pending', 'in_progress'],
        **{item_type: item}
    ).first()

    if existing:
        messages.info(request, _('You already have a pending request for this item.'))
        return redirect('profile')

    # Получаем профиль и его предпочтения
    try:
        profile = request.user.profile
        preferred_methods = profile.preferred_contact_methods
    except Exception as e:
        logger.error(f"Error accessing profile: {e}")
        messages.error(request, _('Profile error. Please update your profile.'))
        return redirect('profile')

    try:
        conn_req = ConnectionRequest.objects.create(
            user=request.user,
            **{item_type: item},
            contact_method=','.join(preferred_methods) if preferred_methods else 'email',
            status='pending',
        )
        logger.debug(f"Quick connect request created: {conn_req.id}")
        messages.success(request, _('Request sent! A manager will contact you via your preferred method.'))
    except Exception as e:
        logger.error(f"Error creating quick connect request: {e}")
        messages.error(request, _('Error creating request.'))

    return redirect('profile')


@login_required
def cancel_connection_request(request, request_id):
    """Отменить заявку (пользователь)"""
    conn_req = get_object_or_404(ConnectionRequest, id=request_id, user=request.user)
    if conn_req.status in ['pending', 'in_progress']:
        conn_req.status = 'cancelled'
        conn_req.save()
        messages.success(request, _('Request cancelled.'))
    else:
        messages.error(request, _('Cannot cancel processed request.'))
    return redirect('profile')


@login_required
def change_tariff(request, tariff_id):
    new_tariff = get_object_or_404(Tariff, id=tariff_id)
    profile = request.user.profile

    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')
    country = Country.objects.filter(id=selected_country_id).first()
    city = City.objects.filter(id=selected_city_id).first()

    current_sub = Subscription.objects.filter(user=request.user, is_active=True).first()
    if current_sub and current_sub.tariff == new_tariff:
        messages.info(request, _('You already have this tariff.'))
        return redirect('profile')

    price = new_tariff.get_price_for_location(country, city)
    if profile.balance >= price:
        try:
            if current_sub:
                current_sub.is_active = False
                current_sub.save()
            subscription = Subscription.objects.create(
                user=request.user,
                tariff=new_tariff,
                is_active=True,
                auto_renew=True,
            )
            profile.balance -= price
            profile.save()
            Payment.objects.create(
                user=request.user,
                subscription=subscription,
                amount=price,
                currency='USD',
                transaction_type=Payment.TransactionType.PAYMENT,
                status=Payment.Status.SUCCEEDED,
                payment_method='balance',
                transaction_id=f"balance_{subscription.id}",
                payment_data={}
            )
            messages.success(request, _('Tariff changed successfully.'))
        except Exception as e:
            logger.error(f"Error changing tariff: {e}")
            messages.error(request, _('Error processing request.'))
    else:
        messages.error(request, _('Insufficient balance.'))
    return redirect('profile')


@login_required
def purchase_separately(request, separately_id):
    separately = get_object_or_404(Separately, id=separately_id)
    profile = request.user.profile

    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')
    country = Country.objects.filter(id=selected_country_id).first()
    city = City.objects.filter(id=selected_city_id).first()

    price = separately.get_price_for_location(country, city)

    if profile.balance >= price:
        try:
            profile.balance -= price
            profile.save()
            Payment.objects.create(
                user=request.user,
                amount=price,
                currency='USD',
                transaction_type=Payment.TransactionType.PAYMENT,
                status=Payment.Status.SUCCEEDED,
                payment_method='balance',
                transaction_id=f"separately_{separately.id}_{profile.user.id}",
                payment_data={}
            )
            messages.success(request, _('Purchase successful.'))
        except Exception as e:
            logger.error(f"Error purchasing separately: {e}")
            messages.error(request, _('Error processing purchase.'))
    else:
        messages.error(request, _('Insufficient balance.'))
    return redirect('profile')


@login_required
def purchase_packets(request, packet_id):
    packets = get_object_or_404(Packets, id=packet_id)
    profile = request.user.profile

    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')
    country = Country.objects.filter(id=selected_country_id).first()
    city = City.objects.filter(id=selected_city_id).first()

    price = packets.get_price_for_location(country, city)

    if profile.balance >= price:
        try:
            profile.balance -= price
            profile.save()
            Payment.objects.create(
                user=request.user,
                amount=price,
                currency='USD',
                transaction_type=Payment.TransactionType.PAYMENT,
                status=Payment.Status.SUCCEEDED,
                payment_method='balance',
                transaction_id=f"packet_{packets.id}_{profile.user.id}",
                payment_data={}
            )
            messages.success(request, _('Purchase successful.'))
        except Exception as e:
            logger.error(f"Error purchasing packet: {e}")
            messages.error(request, _('Error processing purchase.'))
    else:
        messages.error(request, _('Insufficient balance.'))
    return redirect('profile')