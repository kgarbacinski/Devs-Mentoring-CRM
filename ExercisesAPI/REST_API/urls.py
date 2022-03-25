from django.urls import path
from .views import ExerciseView

urlpatterns = [
    path('exercise/', ExerciseView.as_view(), name="exercise"),

]
