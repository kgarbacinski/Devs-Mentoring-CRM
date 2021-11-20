from rest_framework import serializers

from Meetings_calendar.models import Meeting, Note
from Account_management.models import Mentor


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
    def get_subtopic_name(self, obj) -> SubTopic:
        subtopic = self.context.get('subtopic')
        return subtopic.name

    class Meta:
        model = Mentor
        fields = ['id', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = instance.user.student.__str__()
        return representation

    def has_access(self, obj) -> bool:
        subject = self.context.get('subject')
        subtopics = SubTopic.objects.filter(subject=subject).all()
        if not subtopics:
            return False
        user = User.objects.get(id=obj.id)

class AddMeetingSerializer(serializers.ModelSerializer):
    # mentor = serializers.HiddenField(default=serializers.CurrentUserDefault())

        for subtopic in subtopics:
            users_set = subtopic.user.all()
            if user not in users_set:
                return False

        return True

    def get_subtopic_name(self, obj) -> Subject:
        subject = self.context.get('subject')
        return subject.name

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


class GetMeetingSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime("%Y-%m-%d")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation

    class Meta:
        model = Meeting
        fields = '__all__'