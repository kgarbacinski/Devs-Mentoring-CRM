from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class LogIn(View):
    template_name = 'Account_management/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Index(View):
    template_name = 'Account_management/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

