from rest_framework import serializers

from Meetings_calendar.models import Meeting, Note
from Account_management.models import Mentor, Student
from django.contrib.auth.models import User
from rest_framework import serializers
from Files_organizer.models import Document, SubTopic, Subject


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.meeting.date.strftime("%d-%m-%Y")
        representation['hour'] = instance.meeting.date.strftime("%H:%M")
        return representation


class AllMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['mentor'] = instance.mentor.__str__()
        representation['student'] = instance.student.__str__()
        representation['date'] = instance.date.strftime("%d-%m-%Y")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation


class MeetingsMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['person'] = instance.student.__str__()
        representation['mentor'] = instance.mentor.id
        representation['student'] = instance.student.id
        representation['date'] = instance.date.strftime("%Y-%m-%d")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation


class MeetingsStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['person'] = instance.mentor.__str__()
        representation['mentor'] = instance.mentor.id
        representation['student'] = instance.student.id
        representation['date'] = instance.date.strftime("%Y-%m-%d")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__' # ['id', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = instance.user.student.__str__()
        representation['email'] = instance.user.email
        representation['enrolment'] = instance.user.student.enrollmentDate.strftime("%Y-%m-%d")
        representation['path'] = instance.user.student.path.name
        return representation


class AddMeetingSerializer(serializers.ModelSerializer):
    # mentor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Meeting
        fields = '__all__'


class AddNoteSerializer(serializers.ModelSerializer):
    # mentor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['meeting'] = instance.meeting.id
        return representation


class ChangeStudentAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ChangeMentorAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


class GetMeetingSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime("%Y-%m-%d")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation

    class Meta:
        model = Meeting
        fields = '__all__'

class SubTopicSerializer(serializers.ModelSerializer):
    model = SubTopic
    fields = ['name', 'description']


class DocumentSerializer(serializers.ModelSerializer):
    subtopic_name = serializers.CharField(read_only=True, source="subtopic.name")
    subtopic_description = serializers.CharField(read_only=True, source="subtopic.description")

    class Meta:
        model = Document
        fields = ['name', 'docfile', 'type', 'subtopic_name', 'subtopic_description']


class AccessToFileSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField('has_access')
    subtopic_name = serializers.SerializerMethodField('get_subtopic_name')

    def has_access(self, obj) -> bool:
        subtopic = self.context.get('subtopic')
        user = User.objects.get(id=obj.id)
        users_set = subtopic.user.all()
        return user in users_set

    def get_subtopic_name(self, obj) -> SubTopic:
        subtopic = self.context.get('subtopic')
        return subtopic.name

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'access', 'subtopic_name']


class AccessToSubjectSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField('has_access')
    subject_name = serializers.SerializerMethodField('get_subtopic_name')

    def has_access(self, obj) -> bool:
        subject = self.context.get('subject')
        subtopics = SubTopic.objects.filter(subject=subject).all()
        if not subtopics:
            return False
        user = User.objects.get(id=obj.id)

        for subtopic in subtopics:
            users_set = subtopic.user.all()
            if user not in users_set:
                return False

        return True

    def get_subtopic_name(self, obj) -> Subject:
        subject = self.context.get('subject')
        return subject.name

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'access', 'subject_name']


class UserSearchBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']