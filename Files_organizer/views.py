from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from Files_organizer.models import ProgrammingPath, Subject, SubTopic


class ProgramPathView(LoginRequiredMixin,ListView):
    model = ProgrammingPath
    template_name = 'Files_organizer/files-start.html'
    context_object_name = "paths"

class SubjectView(LoginRequiredMixin, DetailView):
    model = ProgrammingPath
    template_name = 'Files_organizer/subject-choice.html'
    slug_url_kwarg = 'path'
    slug_field = 'slug'

# Create your views here.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.get_object()
        subject = Subject.objects.filter(programming_path__name=path).all()
        context['subjects'] = subject
        return context

class SubTopicView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'Files_organizer/subtopic-choice.html'
    slug_url_kwarg = 'subject'
    slug_field = 'slug'
    context_object_name = 'subject'

    def get_object(self, *args, **kwargs):
        path = get_object_or_404(ProgrammingPath, slug__iexact=self.kwargs['path'])
        return self.model.objects.filter(programming_path=path).filter(slug=self.kwargs['subject']).first()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        context['subjects'] = Subject.objects.filter(programming_path=subject.programming_path).all()
        context['subtopics'] = SubTopic.objects.filter(subject=subject).all()

        return context




