from django.db import models
from django.contrib.gis.db import models as gis_models

from django.conf import settings

from trip_planner.trips.models import Trip

# Create your models here.


class Marker(gis_models.Model):
    """
    A map marker with title and location.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    title = models.CharField('Marker title', max_length=100, help_text='This is the title of your map marker.')
    point_location = gis_models.PointField()

    def __str__(self) -> str:
        """Return string representation."""
        return self.title
