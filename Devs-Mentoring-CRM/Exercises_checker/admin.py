from django.contrib import admin
from Exercises_checker.models import Language, Exercise, ExerciseStatus

admin.site.register([Language, Exercise, ExerciseStatus])
