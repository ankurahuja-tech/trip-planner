from django.conf import settings
from django.db import models

from trip_planner.core.models import TimeStampedModel


class Trip(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Trip title', max_length=100, help_text='This is the title of your trip.')
    start_date = models.DateField('Trip start date', help_text='This is the start date of your trip.')
    end_date = models.DateField('Trip end date', help_text='This is the end date of your trip.')
    notes = models.TextField('Trip notes', help_text='These are your notes regarding the trip.', default='')
    # add locations for the trip when the map app is up TODO
    # location =
    # add photos TODO
    # photo =
    # consider: past/ongoing/future choices TODO
    # consider: budget field / app TODO

    def __str__(self) -> str:
        return self.title


class TripDay(TimeStampedModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField('date', help_text='This is a date within the trip.')  # add default values from Trip TODO
    notes = models.TextField('Day notes', help_text='These are your notes for the day of the trip.', default='')


# class Activity(TimeStampedModel):
#     day = models.ForeignKey(TripDay, on_delete=models.CASCADE)
#     title = models.CharField('Activity title', max_length=255, help_text='This is the title of your activity.')
#     description = models.TextField('Activity description', help_text='This is the description of the activity.', null=True, blank=True, unique=True)
#     time = models.TimeField('Activity time', help_text='This is the time of the activity.')
