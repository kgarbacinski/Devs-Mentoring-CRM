from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(), label= 'E-mail')
    password = forms.CharField(widget=forms.PasswordInput(), label = 'Password')

    class Meta:
        model = User
        fields = ['email', 'password']

