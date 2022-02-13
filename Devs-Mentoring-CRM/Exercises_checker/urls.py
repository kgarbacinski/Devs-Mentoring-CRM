from django.urls import path

from Exercises_checker.views import TasksListView, TestToken

urlpatterns = [
    path("", TasksListView.as_view(), name="tasks_list"),
    path("test/", TestToken.as_view(), name="token_test")
]
