from rest_framework import serializers
from Files_organizer.models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['date'] = instance.meeting.date.strftime("%d-%m-%Y")
    #     representation['hour'] = instance.meeting.date.strftime("%H:%M")
    #     return representation