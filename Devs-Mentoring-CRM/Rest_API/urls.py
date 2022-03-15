from django.urls import path, re_path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (AddMeeting, ChangeAvatar, CreateTokenBaseView,
                    DocumentView, EditDeleteMeeting, EditDeleteNote,
                    ExerciseCodeView, ExerciseView, HasAccessToFileView,
                    HasAccessToSubjectView, ListMeetings, ListMeetingsByDates,
                    ListNotes, ListStudents, MeetingDetail,
                    UserSearchBoxSubjectView, UserSearchBoxSubtopicView)

url_token_pattern = [path('token/', CreateTokenBaseView.as_view(), name='token_obtain_pair'),
                     path(
                         'token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
                     path('token/verify/', TokenVerifyView.as_view(),
                          name='token_verify')
                     ]

url_access_pattern = [
    re_path('^access/files/(?P<pk>.+)/$',
            HasAccessToFileView.as_view(), name='file_access'),
    re_path('^access/subject/(?P<pk>.+)/$',
            HasAccessToSubjectView.as_view(), name='subject_access'),
    re_path('^access/searchbox/subtopic/(?P<pk>.+)/$', UserSearchBoxSubtopicView.as_view(),
            name='subtopic_searchbox'),
    re_path('^access/searchbox/subject/(?P<pk>.+)/$', UserSearchBoxSubjectView.as_view(),
            name='subject_searchbox'),
    path("access/exercises/<int:pk>",
         ExerciseView.as_view(), name="exercise_access"),
    path("access/exercises/code/<int:pk>",
         ExerciseCodeView.as_view(), name="exercise_code"),
]


urlpatterns = [
    re_path('^files/(?P<pk>.+)/$', DocumentView.as_view(), name='documents'),

    path('meetings/', ListMeetings.as_view(), name='meetings'),
    # path('all-meetings/', ListAllMeetings.as_view(), name='all_meetings'),
    path('meetings-range/', ListMeetingsByDates.as_view(),
         name='meetings-range'),
    path('meeting/', MeetingDetail.as_view(), name='meeting'),
    path('notes/', ListNotes.as_view(), name='notes'),
    path('edit-note/<int:pk>/',
         EditDeleteNote.as_view(), name='editNote'),
    path('students/', ListStudents.as_view(), name='students'),
    path('add-meeting/', AddMeeting.as_view(), name='add_meeting'),
    path('edit-meeting/<int:pk>/',
         EditDeleteMeeting.as_view(), name='edit_meeting'),
    path('change-avatar/<int:pk>/',
         ChangeAvatar.as_view(), name='change_avatar'),
] + url_token_pattern + url_access_pattern
