from django.urls import path, re_path, include
from rest_framework import routers

from Rest_API.views import DocumentView, HasAccessToFileView, HasAccessToSubjectView, UserSearchBoxSubtopicView, UserSearchBoxSubjectView

urlpatterns = [
    re_path('^files/(?P<pk>.+)/$', DocumentView.as_view(), name='documents'),
    re_path('^access/files/(?P<pk>.+)/$', HasAccessToFileView.as_view(), name='file_access'),
    re_path('^access/subject/(?P<pk>.+)/$', HasAccessToSubjectView.as_view(), name='subject_access'),
    re_path('^access/searchbox/subtopic/(?P<pk>.+)/$', UserSearchBoxSubtopicView.as_view(), name='subtopic_searchbox'),
    re_path('^access/searchbox/subject/(?P<pk>.+)/$', UserSearchBoxSubjectView.as_view(), name='subject_searchbox'),




]
