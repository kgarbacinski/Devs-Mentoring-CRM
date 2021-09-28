from django.urls import path
from .views import Calendar


urlpatterns = [
    path('', Calendar.as_view(), name='calendar')
]