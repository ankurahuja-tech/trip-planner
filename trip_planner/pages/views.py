from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Home Page Views


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"
