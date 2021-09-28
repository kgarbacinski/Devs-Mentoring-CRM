from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import Index, LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', Index.as_view(), name='index'),
]
