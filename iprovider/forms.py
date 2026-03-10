from django import forms
from .models import ConnectionRequest, Profile,SupportTicket
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
import re
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()

class ConnectionRequestForm(forms.ModelForm):
    """Форма заявки"""
    class Meta:
        model = ConnectionRequest
        fields = ['tariff', 'separately', 'packet', 'vacancy', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class UsernameChangeForm(forms.ModelForm):
    """Форма смены имени пользователя"""
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(_('This username is already taken.'))
        return username

def validate_phone(value):
    digits = re.sub(r'\D', '', value)
    if not (5 <= len(digits) <= 15):
        raise ValidationError(_('Phone number must contain 5 to 15 digits.'))
    if not re.match(r'^\+?\d+$', re.sub(r'[\s\-()]', '', value)):
        raise ValidationError(_('Invalid phone number format.'))

class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля"""
    username = forms.CharField(
        max_length=150,
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    preferred_contact_methods = forms.MultipleChoiceField(
        choices=[
            ('email', 'Email'),
            ('whatsapp', 'WhatsApp'),
            ('telegram', 'Telegram'),
            ('phone_call', 'Call'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label=_('Preferred contact methods')
    )

    class Meta:
        model = Profile
        fields = ['address', 'city']  # поле phone убрано – управляется через отдельную страницу
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
        if self.instance and self.instance.pk and self.instance.preferred_contact_methods:
            self.fields['preferred_contact_methods'].initial = self.instance.preferred_contact_methods

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data['username']
            if commit:
                self.user.save()
        profile.preferred_contact_methods = self.cleaned_data['preferred_contact_methods']
        if commit:
            profile.save()
        return profile

class PhoneNumberForm(forms.Form):
    """Форма для добавления номера телефона"""
    number = PhoneNumberField(label=_('Phone number'), widget=forms.TextInput(attrs={'class': 'form-control'}))

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your email')}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Subject')}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('Your message')}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['name'].initial = self.user.get_full_name() or self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True