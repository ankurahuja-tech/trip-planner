import folium

from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

# class MapView(LoginRequiredMixin, ListView):

#     m = folium.Map(location=[42.3601, -71.0589], zoom_start=12)
#     m.save()