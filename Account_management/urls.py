from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import IndexView, LoginView, PaymentView,payment_details

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path("fail", IndexView.as_view()),
    path("success", IndexView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path("payment_details/<uuid:payment_id>", payment_details, name='payment-details'),
    path("payments/", include("payments.urls")),
]