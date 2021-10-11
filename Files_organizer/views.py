from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render

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
        # subject = Subject.objects.filter(programming_path=path).first()
        # print(subject)
        subtopic = SubTopic.objects.filter(subject__programming_path__name=path).all()
        print(subtopic)
        context['subtopics'] = subtopic
        print(context)
        # context['subtopics'] = SubTopic.objects.filter(subject.path=context['subjects'][0]).all()

        return context

class SubTopicView(DetailView):
    model = Subject
    queryset = Subject.objects.all()
    template_name = 'Files_organizer/files_details.html'
    slug_url_kwarg = 'subject'
    slug_field = 'slug'



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        print(self.queryset)

        try:
            subject = self.get_object()
        except :
            subject = self.get_object()[0]
            print('sss')
        # print(subject.programming_path)
        context['subjects'] = Subject.objects.filter(programming_path=subject.programming_path).all()
        # topics = SubTopic.objects.filter(subject=subject).all()
        # print(topics[0].programming_path)
        context['subtopics'] = SubTopic.objects.filter(subject=subject).all()
        print(context)
        return context




