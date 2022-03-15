from re import S
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import ExerciseStatus, Language, Exercise
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


class TasksListView(LoginRequiredMixin, ListView):
    template_name = 'Exercises_checker/task-list.html'
    model = Language
    context_object_name = "languages"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = ExerciseStatus
    context_object_name = "exercise_status"
    template_name = "Exercises_checker/task-detail.html"


    def get_object(self, queryset=None): 
        exercise_status = ExerciseStatus.objects.filter(user=self.request.user).filter(exercise__id=self.kwargs['pk']).first()
        if not exercise_status:
            raise Http404
        return exercise_status






