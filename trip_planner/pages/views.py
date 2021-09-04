from django.views.generic.base import TemplateView

# Home Page Views


class HomePageView(TemplateView):
    template_name = "pages/home.html"
