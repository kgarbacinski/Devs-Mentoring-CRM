from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from Exercises_checker.models import Language, Exercise


class TasksListView(ListView):
    template_name = 'Exercises_checker/task-list.html'
    model = Language
    context_object_name = "languages"




