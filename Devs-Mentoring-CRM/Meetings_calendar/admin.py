from django.contrib import admin
from .models import Mentor, Student

from django.contrib import admin
from .models import Meeting, Note


# Register your models here.
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['date', 'mentor', 'student']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'text']
