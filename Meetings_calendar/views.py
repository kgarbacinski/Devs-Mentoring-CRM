from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class Index(View):
    template_name = 'Meetings_calendar/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

