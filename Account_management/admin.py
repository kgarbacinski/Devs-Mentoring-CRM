from django.contrib import admin
from .models import Mentor, Student


# Register your models here.
@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_mentor']
    list_display_links = ['user']

    def get_mentor(self, instance):
        return [mentor.user for mentor in instance.mentor.all()]
