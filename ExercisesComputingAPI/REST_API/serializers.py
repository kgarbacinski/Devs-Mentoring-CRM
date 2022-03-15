from rest_framework import serializers
from .models import ExerciseTest


class ExerciseTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseTest
        exclude = ('id', 'exercise')
