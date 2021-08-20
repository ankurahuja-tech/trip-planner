from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.urls.base import reverse

from trip_planner.trips.models import Trip

# Create your models here.


class Marker(gis_models.Model):
    """
    A map marker with name and location.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField("Marker name", max_length=100, help_text="This is the name of your map marker.")
    geom = gis_models.GeometryField("Marker", help_text="This is the location point or area of your map marker.")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("markers:marker_list", kwargs={"trip_pk": self.trip.pk})
