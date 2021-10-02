from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from Account_management.exceptions import WrongPassword


class LoginForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'email': 'email_login',
        'password': 'password'
    }
    email = forms.CharField(widget=forms.EmailInput(), label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def validate_password(self, user):
        password = self.cleaned_data.get('password')
        validator = user.check_password(password)
        if not validator:
            raise WrongPassword

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name)
        return super(LoginForm, self).add_prefix(field_name)

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email_login")
        print(email)
        try:

            user = User.objects.get(email=email)
            self.validate_password(user)

        except (User.DoesNotExist, WrongPassword) as e:
            self._errors["email_login"] = self.error_class(["Wrong email or password"])

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password']



class ResetRequestForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(), label='E-mail')

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)

        except (User.DoesNotExist) as e:
            self._errors["email"] = self.error_class(["Email doesn't exist"])

        return self.cleaned_data

