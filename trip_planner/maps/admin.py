from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Marker

# Register your models here.


@admin.register(Marker)
class MarkerAdmin(LeafletGeoAdmin):
    list_display = (
        "id",
        "name",
        "geom",
        "trip",
        "user",
    )
