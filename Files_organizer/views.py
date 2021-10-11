from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView
from Files_organizer.models import ProgrammingPath, Subject, SubTopic


class ProgramPathView(LoginRequiredMixin,ListView):
    model = ProgrammingPath
    template_name = 'Files_organizer/files-start.html'
    context_object_name = "paths"

class SubjectView(DetailView):
    model = ProgrammingPath
    template_name = 'Files_organizer/files.html'
    slug_url_kwarg = 'path'
    slug_field = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.get_object()
        subtopic = SubTopic.objects.filter(subject__programming_path__name=path).all()
        context['subtopics'] = subtopic
        return context

class SubTopicView(DetailView):
    model = Subject
    template_name = 'Files_organizer/files_details.html'
    slug_url_kwarg = 'subject'
    slug_field = 'slug'

    def get_object(self, *args, **kwargs):
        path = get_object_or_404(ProgrammingPath, slug__iexact=self.kwargs['path'])
        return self.model.objects.filter(programming_path__slug=path).all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        context['subtopics'] = SubTopic.objects.filter(subject=subject).all()
        return context




