from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import IndexView, LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
]
