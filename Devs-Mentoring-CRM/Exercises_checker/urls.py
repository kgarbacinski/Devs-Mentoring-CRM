from django.urls import path

from .views import TasksListView, TaskDetailView

urlpatterns = [
    path("", TasksListView.as_view(), name="tasks-list"),
    path("<pk>/", TaskDetailView.as_view(), name="task-detail"),
]
