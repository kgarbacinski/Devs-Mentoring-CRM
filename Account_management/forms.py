from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from Account_management.exceptions import WrongPassword


class LoginForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'login-email'}), label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'login-passoword'}), label='Password')

    def validate_password(self, user):
        password = self.cleaned_data.get('password')
        validator = user.check_password(password)
        if not validator:
            raise WrongPassword

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        try:

            user = User.objects.get(email=email)
            self.validate_password(user)

        except (User.DoesNotExist, WrongPassword) as e:
            self._errors["email"] = self.error_class(["Wrong email or password"])

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password']


class ResetRequestForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'reset-email'}), label='E-mail')

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)

        except (User.DoesNotExist) as e:
            self._errors["email"] = self.error_class(["Email doesn't exist"])

        return self.cleaned_data
