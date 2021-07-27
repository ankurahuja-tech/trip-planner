from django.shortcuts import render
from django.views.generic.base import TemplateView


class CalendarView(TemplateView):
    template_name = 'calendars/calendar.html'


# i think CalendarView needs to be ListView with models: Trip, Day, Activity. TODO
