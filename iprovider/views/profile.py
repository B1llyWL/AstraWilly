"""Профиль и смена имени"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from iprovider.models import Profile, Subscription, Payment, ConnectionRequest
from iprovider.forms import UsernameChangeForm, UserProfileForm

User = get_user_model()

@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    user = request.user

    # Получаем или создаем профиль
    profile, created = Profile.objects.get_or_create(user=user)

    # Активные подписки (для карточки "Active Subscriptions")
    active_subscriptions = Subscription.objects.filter(
        user=user,
        is_active=True
    ).select_related('tariff').order_by('-start_date')

    # Последние платежи (для карточки "Recent Payments")
    payments = Payment.objects.filter(
        user=user
    ).order_by('-created_at')[:5]

    # Все заявки пользователя (для секции "My Requests")
    connection_requests = ConnectionRequest.objects.filter(
        user=user
    ).order_by('-created_at')

    # Словарь для преобразования ключей в названия
    method_names = {
        'email': 'Email',
        'whatsapp': 'WhatsApp',
        'telegram': 'Telegram',
        'phone_call': 'Call',
    }
    # Преобразуем список методов
    display_methods = [method_names.get(m, m) for m in profile.preferred_contact_methods]

    context = {
        'profile': profile,
        'active_subscriptions': active_subscriptions,
        'payments': payments,
        'connection_requests': connection_requests,
        'display_methods': display_methods,
    }
    return render(request, 'iprovider/profile.html', context)


class UsernameChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsernameChangeForm
    template_name = 'account/change_username.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully.'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    return render(request, 'iprovider/edit_profile.html', {'form': form})