from rest_framework import serializers


from Meetings_calendar.models import Meeting, Note
from Account_management.models import Mentor, Student


class NoteSerializer(serializers.ModelSerializer):
    # notes = serializers.PrimaryKeyRelatedField(many=True, queryset=Meeting.objects.all())
    class Meta:
        model = Note
        # fields = ('notes', 'author')
        fields = '__all__'
        # fields = ('notes', 'title')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.meeting.date.strftime("%d-%m-%Y")
        representation['hour'] = instance.meeting.date.strftime("%H:%M")
        return representation


class MeetingsMentorSerializer(serializers.ModelSerializer):
    # notes = NoteSerializer(many=True)
    # notes = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Note.objects.all())
    class Meta:
        model = Meeting
        fields = '__all__'
        # fields = ['student', 'isMentor']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['person'] = instance.student.__str__()
        representation['mentor'] = instance.mentor.user_id
        representation['student'] = instance.student.user_id
        representation['date'] = instance.date.strftime("%d-%m-%Y")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation


class MeetingsStudentSerializer(serializers.ModelSerializer):
    # notes = NoteSerializer(many=True)
    # notes = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Note.objects.all())
    class Meta:
        model = Meeting
        fields = '__all__'
        # fields = ('student', 'mentor', 'date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['person'] = instance.mentor.__str__()
        representation['mentor'] = instance.mentor.user.id
        representation['student'] = instance.student.user.id
        representation['date'] = instance.date.strftime("%d-%m-%Y")
        representation['hour'] = instance.date.strftime("%H:%M")
        return representation


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        # fields = '__all__'
        fields = ['id',]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = instance.user.student.__str__()
        return representation