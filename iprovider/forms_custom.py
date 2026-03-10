from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

"""
try:
    from captcha.fields import ReCaptchaField
    from captcha.widgets import ReCaptchaV2Checkbox
except ImportError:
    from django_recaptcha.fields import ReCaptchaField
    from django_recaptcha.widgets import ReCaptchaV2Checkbox
"""

User = get_user_model()

class CustomSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        strip=False,
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match."))
        return password2

    def signup(self, request, user):
        """Метод, вызываемый allauth после создания пользователя"""
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.save()
