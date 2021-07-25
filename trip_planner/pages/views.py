from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"
