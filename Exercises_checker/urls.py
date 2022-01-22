from django.urls import path

from Exercises_checker.views import TasksListView

urlpatterns = [ path("", TasksListView.as_view(), name="tasks_list")

]