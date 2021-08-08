from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class MapView(LoginRequiredMixin, TemplateView):

    template_name = 'maps/map.html'
