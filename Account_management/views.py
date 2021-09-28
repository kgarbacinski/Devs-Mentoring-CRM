from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from .forms import LoginForm

# Create your views here.

class LoginView(FormView):
    template_name = 'Account_management/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return render(request, self.template_name, {'form': self.form_class()})

    def form_valid(self, form):
        """Authenticate needs username"""

        # TODO form errors
        user = form.save(commit=False)
        username = User.objects.get(email=user.email)
        user = authenticate(username=username, password=user.password)
        if user is not None:
            return redirect('index')
        else:
            return render(self.request, template_name='test.html')


class Index(View):
    template_name = 'Account_management/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
