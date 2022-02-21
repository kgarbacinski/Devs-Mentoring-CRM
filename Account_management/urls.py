from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from .views import IndexView, LoginView, PaymentView, \
    payment_details, SuccessPaymentView, FailurePaymentView, \
    MentorsSummaryView, MaterialsSummaryView
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path("failure-payment/", FailurePaymentView.as_view(), name='failure'),
    path("success-payment/", SuccessPaymentView.as_view(), name='success'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('mentors-summary/', MentorsSummaryView.as_view(), name='mentors_summary'),
    path('materials-summary/', MaterialsSummaryView.as_view(), name='materials'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path("payment_details/<uuid:payment_id>", payment_details, name='payment-details'),
    path("payments/", include("payments.urls")),
    re_path(r'^favicon\.ico$', favicon_view),
]
