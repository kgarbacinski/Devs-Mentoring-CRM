from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet, generics
from Meetings_calendar.models import Meeting, Note
from Account_management.models import Mentor, Student
from .permissions import MentorAllowAllStudentAllowPartial
from .serializers import NoteSerializer, MeetingsStudentSerializer, MeetingsMentorSerializer


# Create your views here.
class ListMeetings (generics.ListAPIView):

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


class ListNotes(generics.UpdateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Note.objects.filter(author_id=user)
        # me = Meeting.objects.filter(student__user=user).filter(meeting__id=qs.meeting)
        print(qs)
        return Note.objects.filter(author_id=user)
