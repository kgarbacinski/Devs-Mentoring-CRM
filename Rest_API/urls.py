from django.urls import path, include, re_path
from .views import ListNotes, ListMeetings, ListStudents, AddMeeting, EditDeleteMeeting, AddNote, EditDeleteNote, \
    ListAllMeetings, MeetingDetail, DocumentView, HasAccessToFileView, HasAccessToSubjectView, UserSearchBoxSubjectView, \
    UserSearchBoxSubtopicView, ListMeetingsByDates, ChangeAvatar

urlpatterns = [
    re_path('^files/(?P<pk>.+)/$', DocumentView.as_view(), name='documents'),
    re_path('^access/files/(?P<pk>.+)/$', HasAccessToFileView.as_view(), name='file_access'),
    re_path('^access/subject/(?P<pk>.+)/$', HasAccessToSubjectView.as_view(), name='subject_access'),
    re_path('^access/searchbox/subtopic/(?P<pk>.+)/$', UserSearchBoxSubtopicView.as_view(), name='subtopic_searchbox'),
    re_path('^access/searchbox/subject/(?P<pk>.+)/$', UserSearchBoxSubjectView.as_view(), name='subject_searchbox'),
    path('meetings/', ListMeetings.as_view(), name='meetings'),
    path('all-meetings/', ListAllMeetings.as_view(), name='all_meetings'),
    path('meetings-range/', ListMeetingsByDates.as_view(), name='meetings-range'),
    path('meeting/', MeetingDetail.as_view(), name='meeting'),
    path('notes/', ListNotes.as_view(), name='notes'),
    path('add-note/', AddNote.as_view(), name='add_note'),
    path('edit-note/<int:pk>/', EditDeleteNote.as_view(), name='editNote'),
    path('students/', ListStudents.as_view(), name='students'),
    path('add-meeting/', AddMeeting.as_view(), name='add_meeting'),
    path('edit-meeting/<int:pk>/', EditDeleteMeeting.as_view(), name='edit_meeting'),
    path('change-avatar/<int:pk>/', ChangeAvatar.as_view(), name='change_avatar'),
]
