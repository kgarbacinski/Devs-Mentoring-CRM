from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from Exercises_checker.models import Language, Exercise
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


class TasksListView(ListView):
    template_name = 'Exercises_checker/task-list.html'
    model = Language
    context_object_name = "languages"


class TestToken(View):
    def get(self, *args, **kwargs):
        return render(self.request, template_name="Exercises_checker/test-token.html")



