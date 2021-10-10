from django.urls import path, include
from .views import ListNotes, ListMeetings, ListStudents, AddMeeting, EditDeleteMeeting, AddNote, EditDeleteNote, ListAllMeetings
from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# # router.register(r'meetings', ListMeetings, basename='all_meetings')
# router.register(r'notes', ListNotes, basename='all_notes')
# urlpatterns = router.urls


urlpatterns = [

    path('meetings/', ListMeetings.as_view(), name='meetings'),
    path('all-meetings/', ListAllMeetings.as_view(), name='all_meetings'),
    path('notes/', ListNotes.as_view(), name='notes'),
    path('notes-add/', AddNote.as_view(), name='add_note'),
    path('notes-edit/<int:pk>/', EditDeleteNote.as_view(), name='edit_note'),
    path('students/', ListStudents.as_view(), name='students'),
    path('meeting-add/' ,AddMeeting.as_view(), name='add_meeting'),
    path('meeting-edit/<int:pk>/' ,EditDeleteMeeting.as_view(), name='edit_meeting'),
]
