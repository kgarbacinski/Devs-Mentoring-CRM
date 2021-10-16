from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, generics, ReadOnlyModelViewSet
from Meetings_calendar.models import Meeting, Note
from Account_management.models import Mentor, Student
from . import serializers
from .permissions import MentorCreate, MentorAllowAllStudentAllowPartial
from .serializers import NoteSerializer, MeetingsStudentSerializer, MeetingsMentorSerializer, StudentsSerializer, \
    AddMeetingSerializer, AddNoteSerializer, AllMeetingSerializer, GetMeetingSerializer


# Create your views here.
# class MeetingsViewSet(ReadOnlyModelViewSet):
#
#     def get_serializer_class(self):
#         user = self.request.user
#         if user.groups.filter(name='Student').exists():
#             return MeetingsStudentSerializer
#         else:
#             return MeetingsMentorSerializer
#
#     def get_queryset(self):
#         month = self.request.GET.get('date')
#         user = self.request.user
#         if user.groups.filter(name='Student').exists():
#             return Meeting.objects.filter(student__user=user).filter(date__month=month)
#         return Meeting.objects.filter(mentor__user=user).filter(date__month=month)
#
#
#     @action(detail=False)
#     def get_list(self, request):
#         pass
#
#     @action(detail=True)
#     def get_meeting(self, request, pk=None):
#         query = Meeting.objects.get(id=pk)
#         return Response()  #
#
#     @action(detail=True, methods=['post', 'delete'])
#     def delete_meeting(self, request, pk=None):
#         pass


class ListMeetings(generics.ListAPIView):

    def get_serializer_class(self):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return MeetingsStudentSerializer
        else:
            return MeetingsMentorSerializer

    def get_queryset(self):
        month = self.request.GET.get('date')
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Meeting.objects.filter(student__user=user).filter(date__month=month)
        return Meeting.objects.filter(mentor__user=user).filter(date__month=month)


class MeetingDetail(generics.ListAPIView):
    serializer_class = GetMeetingSerializer

    def get_queryset(self):
        meeting = self.request.GET.get('id')
        user = self.request.user
        return Meeting.objects.filter(mentor__user=user).filter(id=meeting)


class ListAllMeetings(generics.ListAPIView):
    serializer_class = AllMeetingSerializer

    def get_queryset(self):
        month = self.request.GET.get('date')
        return Meeting.objects.filter(date__month=month).order_by('mentor', 'date')


class AddMeeting(generics.CreateAPIView):
    permission_classes = [MentorCreate]
    serializer_class = AddMeetingSerializer

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)


class EditDeleteMeeting(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [MentorCreate]
    serializer_class = AddMeetingSerializer

    # queryset = Meeting.objects.all()

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(mentor__user=user)


class ListNotes(generics.ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        meeting = self.request.GET.get('id')
        user = self.request.user
        return Note.objects.filter(author_id=user).filter(meeting_id=meeting)


class AddNote(generics.CreateAPIView):
    serializer_class = AddNoteSerializer


class EditDeleteNote(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddNoteSerializer

    def get_queryset(self, pk=None):
        user = self.request.user
        return Note.objects.all()


class ListStudents(generics.ListAPIView):
    serializer_class = StudentsSerializer

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(mentor__user__username=user)
