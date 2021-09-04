from django.urls import path

from .views import ContactPageView, HomePageView

app_name = "pages"
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("contact/", ContactPageView.as_view(), name="contact"),
]
