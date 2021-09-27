from django.urls import path
from .views import LogIn, Index


urlpatterns = [
    path('', LogIn.as_view(), name='login'),
    path('index/', Index.as_view(), name='index'),
]
