from django.urls import path

from Rest_API.views import DocumentView

urlpatterns = [
    path('files/', DocumentView.as_view(), name='documents'),

]