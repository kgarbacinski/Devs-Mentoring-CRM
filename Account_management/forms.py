from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from Account_management.exceptions import WrongPassword
from Account_management.models import PaymentInfo


class LoginForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'login-email'}), label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'login-password'}), label='Password')
    error_messages = {'email': ' Wrong email or password'}

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

            self._errors["email"] = self.error_messages['email']

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password']


class ResetRequestForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id': 'reset-email'}), label='E-mail')
    error_messages = {'email': "Email doesn't exists"}

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)

        except User.DoesNotExist as e:
            self._errors["email"] = self.error_messages['email']
        return self.cleaned_data


class ResetPasswordForm(SetPasswordForm):
    error_css_class = 'text-error'


class PaymentForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name'}), label='name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'last-name'}), label='last-name')
    companyName = forms.CharField(widget=forms.TextInput(attrs={'id': 'company'}), label='company')
    nip = forms.CharField(widget=forms.TextInput(attrs={'id': 'company-nip'}), label='company-nip')
    street = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'adress', 'placeholder': 'Street and house / flat number'}),
        label='company-nip')
    postCode = forms.CharField(widget=forms.TextInput(attrs={'id': 'post-code'}), label='post-code')
    town = forms.CharField(widget=forms.TextInput(attrs={'id': 'city'}), label='city')
    phone = PhoneNumberField(region='PL', widget=forms.TextInput(
        attrs={'id': 'phone'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'id': 'email', 'name': 'email'}))
    vat = forms.BooleanField(required=None, widget=forms.CheckboxInput(attrs={'id': 'save'}))

    class Meta:
        model = PaymentInfo
        fields = '__all__'
