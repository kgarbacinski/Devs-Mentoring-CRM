from django.contrib import admin
from .models import Language, Exercise, ExerciseTest

admin.site.register([Language, Exercise, ExerciseTest])
