from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class Calendar(View):
    template_name = 'Meetings_calendar/calendar.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

