from django.urls import path, re_path

from Rest_API.views import DocumentView

urlpatterns = [
    re_path('^files/(?P<pk>.+)/$', DocumentView.as_view()),
    # path("files/<pk>", DocumentView.as_view(), name='documents'),

]

