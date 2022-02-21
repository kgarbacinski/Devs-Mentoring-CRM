from __future__ import annotations
import datetime
import enum
import re
from django.utils import timezone

from typing import Dict, Tuple
from Exercises_checker.models import Language, Exercise, ExerciseStatus
from Meetings_calendar.models import Meeting, Note
from Account_management.models import Student, Mentor, Path
from .permissions import MentorCreate, MentorAccess
from .serializers import NoteSerializer, StudentsSerializer, AddMeetingSerializer, AddNoteSerializer, \
    GetMeetingSerializer, ChangeStudentAvatarSerializer, ChangeMentorAvatarSerializer, \
    MeetingSerializer, PathExerciseSerializer, AllMeetingSerializer, GetMentorsSerializer, GetStudentsSerializer, \
    GetPathsSerializer, GetMeetingDatesSerializer
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from Files_organizer.models import Document, SubTopic, Subject
from Rest_API.permissions import FileAccessPermission
from Rest_API.serializers import DocumentSerializer, AccessToFileSerializer, AccessToSubjectSerializer, \
    UserSearchBoxSerializer


# Create your views here.
class ListMeetings(generics.ListAPIView):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Meeting.objects.filter(student__user=user).filter(date__year=year).filter(
                date__month=month).order_by('date')
        return Meeting.objects.filter(mentor__user=user).filter(date__year=year).filter(date__month=month).order_by(
            'date')


class ListAllMeetings(generics.ListAPIView):
    permission_classes = [MentorAccess]
    serializer_class = AllMeetingSerializer

    def get_queryset(self):
        query_list = Meeting.objects.all()
        user = self.request.user

        if user.groups.filter(name='Moderator').exists():
            mentor = self.request.query_params.get('mentor', None)
        else:
            mentor = Mentor.objects.get(user=user)

        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        day = self.request.query_params.get('day', None)
        student = self.request.query_params.get('student', None)
        path = self.request.query_params.get('path', None)

        if year:
            query_list = query_list.filter(date__year=year)
        if month:
            query_list = query_list.filter(date__month=month)
        if day:
            query_list = query_list.filter(date__day=day)
        if mentor:
            query_list = query_list.filter(mentor=mentor)
        if student:
            query_list = query_list.filter(student=student)
        if path:
            query_list = query_list.filter(path=path)
        return query_list.order_by('date')


class ListMeetingsByDates(generics.ListAPIView):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        start_date = timezone.make_aware(
            datetime.datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d %H:%M'),
            timezone.get_current_timezone())
        end_date = timezone.make_aware(datetime.datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d'),
                                       timezone.get_current_timezone())
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Meeting.objects.filter(student__user=user).filter(date__range=[start_date, end_date]).order_by(
                'date')
        return Meeting.objects.filter(mentor__user=user).filter(date__range=[start_date, end_date]).order_by('date')


class MeetingDetail(generics.ListAPIView):
    serializer_class = GetMeetingSerializer

    def get_queryset(self):
        meeting = self.request.GET.get('id')
        user = self.request.user
        return Meeting.objects.filter(mentor__user=user).filter(id=meeting)


class AddMeeting(generics.CreateAPIView):
    permission_classes = [MentorCreate]
    serializer_class = AddMeetingSerializer

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)

    def perform_create(self, serializer):
        data = self.request.data
        mentor = data['mentor']
        student = data['student']
        date = timezone.make_aware(datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M'),
                                   timezone.get_current_timezone())
        path_id = Student.objects.get(id=student).path.id
        meeting = serializer.save(
            date=date,
            mentor=Mentor.objects.get(id=mentor),
            student=Student.objects.get(id=student),
            path=Path.objects.get(id=path_id))
        Note.objects.create(
            meeting=meeting,
            author=User.objects.get(id=Mentor.objects.get(id=data['mentor']).user.id),
            title='',
            text=data['note'] if 'note' in data else '')
        Note.objects.create(
            meeting=meeting,
            author=User.objects.get(id=Student.objects.get(id=data['student']).user.id),
            title='',
            text='')


class EditDeleteMeeting(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [MentorCreate]
    serializer_class = AddMeetingSerializer

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)

    def perform_update(self, serializer):
        data = self.request.data
        meeting_id = data['id']
        student_id = data['student']
        date = timezone.make_aware(datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M'),
                                   timezone.get_current_timezone())
        path_id = Student.objects.get(id=student_id).path.id
        serializer.save(
            id=meeting_id,
            date=date,
            student=Student.objects.get(id=student_id),
            path=Path.objects.get(id=path_id))

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(mentor__user=user)


class ListNotes(generics.ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self) -> QuerySet[Note]:
        meeting = self.request.GET.get('id')
        user = self.request.user
        return Note.objects.filter(author_id=user).filter(meeting_id=meeting)


class EditDeleteNote(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddNoteSerializer

    def get_queryset(self, pk=None):
        return Note.objects.all()

    def perform_update(self, serializer):
        serializer.save()


class ListStudents(generics.ListAPIView):
    serializer_class = StudentsSerializer

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(mentor__user__username=user)


class GetMeetingDates(generics.ListAPIView):
    serializer_class = GetMeetingDatesSerializer

    def get_queryset(self):
        user = self.request.user
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)

        if user.groups.filter(name='Moderator').exists():
            if year and month:
                return Meeting.objects.filter(date__year=year).filter(date__month=month).dates('date', 'day')
            if year:
                return Meeting.objects.filter(date__year=year).dates('date', 'month')
            return Meeting.objects.dates('date', 'year')

        if year and month:
            return Meeting.objects.filter(mentor__user=user).filter(date__year=year).filter(date__month=month).dates(
                'date', 'day')
        if year:
            return Meeting.objects.filter(mentor__user=user).filter(date__year=year).dates('date', 'month')
        return Meeting.objects.filter(mentor__user=user).dates('date', 'year')


class GetMentorsList(generics.ListAPIView):
    serializer_class = GetMentorsSerializer

    def get_queryset(self):
        all_mentors = Meeting.objects.all()

        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        day = self.request.query_params.get('day', None)
        student = self.request.query_params.get('student', None)
        mentor = self.request.query_params.get('mentor', None)

        if year:
            all_mentors = all_mentors.filter(date__year=year)
        if month:
            all_mentors = all_mentors.filter(date__month=month)
        if day:
            all_mentors = all_mentors.filter(date__day=day)
        if student:
            all_mentors = all_mentors.filter(student_id=student)
        if mentor:
            all_mentors = all_mentors.filter(mentor_id=mentor)

        mentors_set = set(all_mentors.values_list('mentor_id'))

        mentors = [i[0] for i in list(mentors_set)]
        query_paths = Mentor.objects.filter(id__in=mentors)

        return query_paths


class GetStudentsList(generics.ListAPIView):
    serializer_class = GetStudentsSerializer

    def get_queryset(self):
        user = self.request.user
        all_meetings = Meeting.objects.all()

        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        day = self.request.query_params.get('day', None)
        student = self.request.query_params.get('student', None)

        if user.groups.filter(name='Moderator').exists():
            mentor = self.request.query_params.get('mentor', None)
        else:
            mentor = Mentor.objects.get(user=user)

        if year:
            all_meetings = all_meetings.filter(date__year=year)
        if month:
            all_meetings = all_meetings.filter(date__month=month)
        if day:
            all_meetings = all_meetings.filter(date__day=day)
        if student:
            all_meetings = all_meetings.filter(student_id=student)
        if mentor:
            all_meetings = all_meetings.filter(mentor_id=mentor)

        meetings_set = set(all_meetings.values_list('student_id'))

        paths = [i[0] for i in list(meetings_set)]
        query_paths = Student.objects.filter(id__in=paths)
        return query_paths


class GetPathsList(generics.ListAPIView):
    serializer_class = GetPathsSerializer

    def get_queryset(self):
        user = self.request.user
        all_meetings = Meeting.objects.all()

        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        day = self.request.query_params.get('day', None)
        student = self.request.query_params.get('student', None)
        if user.groups.filter(name='Moderator').exists():
            mentor = self.request.query_params.get('mentor', None)
        else:
            mentor = Mentor.objects.get(user=user)

        if year:
            all_meetings = all_meetings.filter(date__year=year)
        if month:
            all_meetings = all_meetings.filter(date__month=month)
        if day:
            all_meetings = all_meetings.filter(date__day=day)
        if student:
            all_meetings = all_meetings.filter(student_id=student)
        if mentor:
            all_meetings = all_meetings.filter(mentor_id=mentor)

        meetings_set = set(all_meetings.values_list('path__id'))

        paths = [i[0] for i in list(meetings_set)]
        query_paths = Path.objects.filter(id__in=paths)
        return query_paths


class ChangeAvatar(generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return ChangeStudentAvatarSerializer
        else:
            return ChangeMentorAvatarSerializer

    def get_queryset(self, pk=None):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Student.objects.all()
        return Mentor.objects.all()


class Patterns:
    whole_name_pattern = r'\w+\s\w+'


class DocumentView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Document]:
        subtopic_id = self.kwargs['pk']
        try:
            subtopic = SubTopic.objects.get(id=subtopic_id)
        except SubTopic.DoesNotExist:
            raise Http404
        users = subtopic.user.all()
        if self.request.user in users or self.request.user.is_superuser or self.request.user.groups.filter(
                name='Mentor').exists():
            documents = Document.objects.filter(subtopic_id=subtopic_id).all()
            if not documents:
                raise Http404
            return documents
        raise PermissionDenied


class HasAccessToFileView(generics.ListAPIView, mixins.DestroyModelMixin, mixins.CreateModelMixin):
    serializer_class = AccessToFileSerializer
    permission_classes = [FileAccessPermission]
    queryset = User.objects.filter(groups__name='Student').all()

    def get_serializer_context(self) -> Dict[str, None | Request | GenericAPIView]:
        context = super().get_serializer_context()
        subtopic_id = self.kwargs['pk']
        try:
            subtopic = SubTopic.objects.get(id=subtopic_id)
        except SubTopic.DoesNotExist:
            raise Http404
        context["subtopic"] = subtopic
        return context

    def __get_subtopic_and_user(self, subtopic_id, user_id) -> Response | Tuple[SubTopic, User]:
        if not subtopic_id or not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            subtopic = SubTopic.objects.get(id=subtopic_id)
            user = User.objects.get(id=user_id)
        except (SubTopic.DoesNotExist, User.DoesNotExist) as e:
            raise Http404
        return subtopic, user

    def post(self, request, *args, **kwargs) -> Response:
        subtopic_id = self.kwargs['pk']
        user_id = request.data
        subtopic, user = self.__get_subtopic_and_user(subtopic_id, user_id)
        subtopic.user.add(user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs) -> Response:
        subtopic_id = self.kwargs['pk']
        user_id = request.data
        subtopic, user = self.__get_subtopic_and_user(subtopic_id, user_id)
        subtopic.user.remove(user)
        return Response(status=status.HTTP_200_OK)


class HasAccessToSubjectView(generics.ListAPIView, mixins.DestroyModelMixin, mixins.CreateModelMixin):
    serializer_class = AccessToSubjectSerializer
    permission_classes = [FileAccessPermission]
    queryset = User.objects.filter(groups__name='Student').all()

    def __get_subject_and_user(self, subject_id, user_id) -> Response | Tuple[Subject, User]:
        if not subject_id or not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            subject = Subject.objects.get(id=subject_id)
            user = User.objects.get(id=user_id)
        except (SubTopic.DoesNotExist, User.DoesNotExist) as e:
            raise Http404
        return subject, user

    def get_serializer_context(self) -> Dict[str, None | Request | GenericAPIView]:
        context = super().get_serializer_context()
        subject = self.kwargs['pk']
        try:
            subject = Subject.objects.get(id=subject)
        except Subject.DoesNotExist:
            raise Http404
        context["subject"] = subject
        return context

    def post(self, request, *args, **kwargs) -> Response:
        subject_id = self.kwargs['pk']
        user_id = request.data
        subject, user = self.__get_subject_and_user(subject_id, user_id)
        subtopics_set = subject.subtopic_set.all()
        for subtopic in subtopics_set:
            subtopic.user.add(user)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs) -> Response:
        subject_id = self.kwargs['pk']
        user_id = request.data
        subject, user = self.__get_subject_and_user(subject_id, user_id)
        subtopics_set = subject.subtopic_set.filter(user=user).all()
        for subtopic in subtopics_set:
            subtopic.user.remove(user)
        return Response(status=status.HTTP_200_OK)


class UserSearchBoxSubtopicView(generics.ListAPIView):
    serializer_class = UserSearchBoxSerializer
    permission_classes = [FileAccessPermission]

    class Access(enum.Enum):
        HAS_ACCESS = "1",
        NO_ACCESS = "0"

        @classmethod
        def from_str(cls, val):
            if val in ("1"):
                return cls.HAS_ACCESS
            elif val in ("0"):
                return cls.NO_ACCESS

    def __get_user_by_name_or_surname_access(self, text, subtopic, filter_by) -> QuerySet[User]:
        if filter_by == 'first_name':
            return User.objects.filter(first_name__contains=text).filter(groups__name='Student').filter(
                subtopic=subtopic).all()

        elif filter_by == "last_name":
            return User.objects.filter(last_name__contains=text).filter(
                groups__name='Student').filter(
                subtopic=subtopic).all()

    def with_access(self, text, subtopic) -> QuerySet[User]:
        filter = self.__get_user_by_name_or_surname_access
        if re.match(Patterns.whole_name_pattern, text):
            space = text.find(" ")
            first_text = text[:space]
            second_text = text[space + 1:]
            queryset = filter(text=first_text, subtopic=subtopic, filter_by="first_name") or \
                       filter(text=second_text, subtopic=subtopic, filter_by="first_name") or \
                       filter(text=first_text, subtopic=subtopic, filter_by="last_name") or \
                       filter(text=second_text, subtopic=subtopic, filter_by='last_name')


        else:
            queryset = filter(text=text, subtopic=subtopic, filter_by="first_name") or \
                       filter(text=text, subtopic=subtopic, filter_by="last_name")

        return queryset

    def __get__user_by_name_or_surname_no_access(self, text, subtopic, filter_by) -> QuerySet[User]:
        if filter_by == 'first_name':
            return User.objects.exclude(subtopic=subtopic).filter(first_name__contains=text).filter(
                groups__name='Student').all()

        elif filter_by == "last_name":
            return User.objects.exclude(subtopic=subtopic).filter(last_name__contains=text).filter(
                groups__name='Student').all()

    def no_access(self, text, subtopic) -> QuerySet[User]:
        filter = self.__get__user_by_name_or_surname_no_access
        if re.match(Patterns.whole_name_pattern, text):
            space = text.find(" ")
            first_text = text[:space]
            second_text = text[space + 1:]
            queryset = filter(text=first_text, subtopic=subtopic, filter_by="first_name") or \
                       filter(text=second_text, subtopic=subtopic, filter_by="first_name") or \
                       filter(text=first_text, subtopic=subtopic, filter_by="last_name") or \
                       filter(text=second_text, subtopic=subtopic, filter_by='last_name')

        else:
            queryset = filter(text=text, subtopic=subtopic, filter_by="first_name") or \
                       filter(text=text, subtopic=subtopic, filter_by="last_name")
        return queryset

    def get_queryset(self) -> QuerySet[User]:
        subtopic_id = self.kwargs['pk']
        text = self.request.GET.get('text')
        access = self.request.GET.get('access')
        access = self.Access.from_str(access)

        try:
            subtopic = SubTopic.objects.get(id=subtopic_id)
        except SubTopic.DoesNotExist:
            raise Http404

        if access == self.Access.HAS_ACCESS:
            return self.with_access(text, subtopic)

        if access == self.Access.NO_ACCESS:
            return self.no_access(text, subtopic)

        raise ValidationError(detail="Access parameter can be 0 or 1")


class UserSearchBoxSubjectView(generics.ListAPIView):
    serializer_class = UserSearchBoxSerializer
    permission_classes = [FileAccessPermission]

    class Access(enum.Enum):
        HAS_ACCESS = "1",
        NO_ACCESS = "0"

        @classmethod
        def from_str(cls, val):
            if val in ("1"):
                return cls.HAS_ACCESS
            elif val in ("0"):
                return cls.NO_ACCESS

    def __get_user_by_name_or_surname_access(self, text, filter_by) -> QuerySet[User]:
        if filter_by == 'first_name':
            return User.objects.filter(first_name__contains=text).filter(groups__name='Student').all()

        elif filter_by == "last_name":
            return User.objects.filter(last_name__contains=text).filter(
                groups__name='Student').all()

    def __iterate_queryset(self, queryset, subtopics, access) -> list:
        if not queryset:
            return queryset
        users_list = list(queryset)

        for user in queryset:
            for subtopic in subtopics:
                users_set = subtopic.user.all()
                if access:
                    if user not in users_set:
                        users_list.remove(user)
                        break
                else:
                    if user not in users_set:
                        break

        return users_list

    def __get_queryset_from_text(self, text, subject) -> Tuple[QuerySet[User], SubTopic]:
        subtopics = SubTopic.objects.filter(subject=subject).all()
        filter = self.__get_user_by_name_or_surname_access
        if re.match(Patterns.whole_name_pattern, text):
            space = text.find(" ")
            first_text = text[:space]
            second_text = text[space + 1:]
            queryset = filter(text=first_text, filter_by="first_name") or \
                       filter(text=second_text, filter_by="first_name") or \
                       filter(text=first_text, filter_by="last_name") or \
                       filter(text=second_text, filter_by='last_name')

        else:
            queryset = filter(text=text, filter_by="first_name") or \
                       filter(text=text, filter_by="last_name")

        return queryset, subtopics

    def with_access(self, text, subject):
        queryset, subtopics = self.__get_queryset_from_text(text, subject)
        return self.__iterate_queryset(queryset, subtopics, True)

    def no_access(self, text, subject):
        queryset, subtopics = self.__get_queryset_from_text(text, subject)
        return self.__iterate_queryset(queryset, subtopics, False)

    def get_queryset(self) -> list:
        subject_id = self.kwargs['pk']
        text = self.request.GET.get('text')
        access = self.request.GET.get('access')
        access = self.Access.from_str(access)

        # print(access)
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise Http404

        if access == self.Access.HAS_ACCESS:
            return self.with_access(text, subject)

        if access == self.Access.NO_ACCESS:
            return self.no_access(text, subject)

        raise ValidationError(detail="Access parameter can be 0 or 1")


class ExerciseView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PathExerciseSerializer

    def get_language_and_user(self):
        language_id = self.kwargs['pk']
        language = get_object_or_404(Language, id=language_id)
        user = self.request.user
        return language, user

    def get_all_exercises_quantity(self):
        language, user = self.get_language_and_user()
        all_exercises_quantity = Exercise.objects.filter(language__user=user).filter(language=language).count()
        done_exercises_quantity = ExerciseStatus.objects.filter(exercise__language=language).filter(user=user).filter(
            done=True).count()

        return all_exercises_quantity, done_exercises_quantity

    def get_queryset_exercise_list(self, type):
        language, user = self.get_language_and_user()
        queryset = ExerciseStatus.objects.filter(exercise__language=language).filter(exercise__type=type).filter(
            user=user).all()
        exercise_quantity = Exercise.objects.filter(language=language).filter(type=type).filter(
            language__user=user).count()
        done_exercise_quantity = queryset.filter(done=True).count()

        return queryset, exercise_quantity, done_exercise_quantity

    def list(self, request, *args, **kwargs):
        all_exercises_quantity, done_exercises_quantity = self.get_all_exercises_quantity()
        easy_exercises, easy_exercises_quantity, done_easy_exercises_quantity = self.get_queryset_exercise_list(
            type="EASY")
        medium_exercises, medium_exercises_quantity, done_medium_exercises_quantity = self.get_queryset_exercise_list(
            type="MEDIUM")
        hard_exercises, hard_exercises_quantity, done_hard_exercises_quantity = self.get_queryset_exercise_list(
            type="HARD")

        return Response({
            "quantity": {
                "all_exercises_quantity": all_exercises_quantity,
                "done_exercises_quantity": done_exercises_quantity,
                "easy_exercises_quantity": easy_exercises_quantity,
                "done_easy_exercises_quantity": done_easy_exercises_quantity,
                "medium_exercises_quantity": medium_exercises_quantity,
                "done_medium_exercises_quantity": done_medium_exercises_quantity,
                "hard_exercises_quantity": hard_exercises_quantity,
                "done_hard_exercises_quantity": done_hard_exercises_quantity,
            },
            "exercises": {
                "easy": self.serializer_class(easy_exercises, many=True).data,
                "medium": self.serializer_class(medium_exercises, many=True).data,
                "hard": self.serializer_class(hard_exercises, many=True).data,
            }
        })
