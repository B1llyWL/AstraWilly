from django.shortcuts import render, redirect, get_object_or_404
from  django.contrib.auth.decorators import login_required
from  django.contrib import messages
from  django.utils.translation import  gettext as _
from  ..models import PhoneNumber
from  ..forms import PhoneNumberForm

@login_required
def phone_list(request):
    """Страница управления номерами телефона"""
    phone_numbers = request.user.phone_numbers.all()
    return render(request, 'account/phone_list.html', {'phone_numbers': phone_numbers})

@login_required
def phone_add(request):
    """Добавление нового номера(с отправкой кода)"""
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            # Проверяем, не существует ли уже такой номер у пользователя
            if PhoneNumber.objects.filter(user=request.user, number=number).exists():
                messages.error(request, _('This number is already added.'))
                return  redirect('phone_list')
            phone = PhoneNumber.objects.create(
                user = request.user,
                number = number,
                verified = False,
                primary = False,
            )
            phone.generate_code()
            # Отправка SMS
            print(f"Verification code for {number}: {phone.verification_code}")
            messages.success(request, _('Verification code sent to your phone.'))
            return  redirect('phone_verify', phone_id=phone.id)
        else:
            print("Form errors:", form.errors)
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PhoneNumberForm()
    return render(request, ' account/phone_add.html', {'form': form})

@login_required
def phone_verify(request, phone_id):
    """Подтверждение номера по коду"""
    phone = get_object_or_404(PhoneNumber, id=phone_id, user=request.user)
    if phone.verified:
        messages.info(request, _('This number is already verified.'))
        return redirect('phone_list')
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == phone.verification_code:
            phone.verified =True
            phone.save()
            messages.success(request, _('Phone number verified successfully.'))
            return  redirect('phone_list')
        else:
            messages.error(request, _('Invalid verification code.'))
    return  render(request, 'account/phone_verify.html', {'phone': phone})

@login_required
def phone_make_primary(request, phone_id):
    """Установить номер основным"""
    phone = get_object_or_404(PhoneNumber, id=phone_id, user=request.user)
    if request.method == 'POST':
            if not phone.verified:
                messages.error(request, _('Cannot set unverified number as primary.'))
                return  redirect('phone_list')
            #Сбрасываем primary number у всех номеров пользователя
            request.user.phone_numbers.update(primary=False)
            phone.primary = True
            phone.save()
            # Обновляем поле phone в Profile
            profile = request.user.profile
            profile.phone = str(phone.number)
            profile.save()
            messages.success(request, _('Primary phone number updated.'))
    return redirect('phone_list')

@login_required
def phone_remove(request, phone_id):
    """Удалить номер"""
    phone = get_object_or_404(PhoneNumber, id=phone_id, user=request.user)
    if request.method == 'POST':
        if phone.primary:
            messages.error(request, _('Cannot remove primary phone number.'))
        else:
            phone.delete()
            messages.success(request, _('Phone number removed.'))
    return redirect('phone_list')

@login_required
def phone_resend(request, phone_id):
    phone = get_object_or_404(PhoneNumber, id=phone_id, user=request.user)
    phone.generate_code()  # генерирует новый код и сохраняет
    print(f"New verification code for {phone.number}: {phone.verification_code}")
    messages.success(request, _('Verification code resent.'))
    return redirect('phone_verify', phone_id=phone.id)