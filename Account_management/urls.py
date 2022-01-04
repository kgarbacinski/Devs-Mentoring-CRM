from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import IndexView, LoginView, PaymentView,payment_details, SuccessPaymentView, FailurePaymentView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path("failure-payment/", FailurePaymentView.as_view(), name='failure'),
    path("success-payment/", SuccessPaymentView.as_view(), name='success'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path("payment_details/<uuid:payment_id>", payment_details, name='payment-details'),
    path("payments/", include("payments.urls")),
]