from django.urls import path

from REST_API.views import TestView

urlpatterns = [
    path('', TestView.as_view()),

]
