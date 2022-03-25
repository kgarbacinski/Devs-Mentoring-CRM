from django.urls import path
from .views import ExerciseView

urlpatterns = [
    path('', ExerciseView.as_view())
]
