from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class ExercisesView(LoginRequiredMixin, View):
    template_name = 'Exercises_checker/task-list.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
