from django.contrib import admin
from Files_organizer.models import ProgrammingPath, Subject, SubTopic, Document


@admin.register(ProgrammingPath)
class ProgrammingPathAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

