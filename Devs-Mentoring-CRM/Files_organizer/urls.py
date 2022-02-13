from django.urls import path

from Files_organizer.views import ProgramPathView, SubjectView, SubTopicView

urlpatterns = [
    path('', ProgramPathView.as_view(), name='storage'),
    path("<slug:path>/", SubjectView.as_view(), name="subject"),
    path("<slug:path>/<slug:subject>/", SubTopicView.as_view(), name="subtopic"),
]