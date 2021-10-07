from django.urls import path, include
from .views import ListNotes, ListMeetings
from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# # router.register(r'meetings', ListMeetings, basename='all_meetings')
# router.register(r'notes', ListNotes, basename='all_notes')
# urlpatterns = router.urls


urlpatterns = [

    path('meetings/', ListMeetings.as_view(), name='meetings'),
    path('notes/', ListNotes.as_view(), name='notes'),
]
