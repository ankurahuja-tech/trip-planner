from django.contrib import admin
from django.contrib.gis import admin as geo_admin
from leaflet.admin import LeafletGeoAdmin

from .models import Marker

# Register your models here.


@admin.register(Marker)
class MarkerAdmin(LeafletGeoAdmin):
    list_display = (
        "id",
        "title",
        "point_location",
        "trip",
        "user",
    )
