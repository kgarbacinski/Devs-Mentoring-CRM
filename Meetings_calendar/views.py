from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class CalendarView(LoginRequiredMixin, View):
    template_name = 'Meetings_calendar/calendar.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('login')
