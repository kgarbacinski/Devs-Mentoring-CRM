from django.contrib.auth.models import User
from rest_framework import serializers
from Files_organizer.models import Document, SubTopic, Subject


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
