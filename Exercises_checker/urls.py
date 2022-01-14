from django.urls import path
from .views import ExercisesView

urlpatterns = [
    path("", ExercisesView.as_view(), name='exercises'),
]
