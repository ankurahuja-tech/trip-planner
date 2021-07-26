from django.conf.urls import url
from django.urls import path
from .views import ProfilePageView

app_name = "accounts"
urlpatterns = [
    path('profile/', ProfilePageView.as_view(), name='profile'),
]
