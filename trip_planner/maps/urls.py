from django.conf.urls import url
from django.urls import path
from .views import MapView

app_name = "maps"
urlpatterns = [
    path('', MapView.as_view(), name='map'),
]
