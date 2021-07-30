import datetime

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

    def create_trip_days(self):
        """
        Creates trip days for a new or updated Trip instance, provided that they are not already created.
        """
        trip_duration = self.end_date - self.start_date

        # get list of dates for the Trip
        trip_dates = []
        for day in range(trip_duration.days + 1):
            trip_date = self.start_date + datetime.timedelta(days=day)
            trip_dates.append(trip_date)

        # create TripDay instance for each day of the Trip
        for trip_date in trip_dates:
            TripDay.objects.get_or_create(trip=self, date=trip_date)

    def update_trip_days_nums(self):
        """
        Update TripDay object's "num" field for each TripDay object a particular Trip.
        """
        trip_days = TripDay.objects.all().filter(trip=self).order_by('date')
        num_increment = 1
        for trip_day in trip_days:
            if trip_day.num != num_increment:
                trip_day.num = num_increment
                trip_day.save(update_fields=['num'])
            num_increment += 1

    def save(self, *args, **kwargs):
        """
        Save Trip object instance in the database and create TripDay objects for each day of the trip.
        """
        super().save(*args, **kwargs)
        self.create_trip_days()
        self.update_trip_days_nums()


class TripDay(TimeStampedModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    num = models.IntegerField(
        'day of the trip', help_text='This shows what day of the trip is this.', blank=True, null=True
    )
    date = models.DateField('date', help_text='This is a date within the trip.')
    notes = models.TextField('Day notes', help_text='These are your notes for the day of the trip.', default='')


# add Activity TODO
# class Activity(TimeStampedModel):
#     day = models.ForeignKey(TripDay, on_delete=models.CASCADE)
#     title = models.CharField('Activity title', max_length=255, help_text='This is the title of your activity.')
#     description = models.TextField('Activity description', help_text='This is the description of the activity.', null=True, blank=True, unique=True)
#     time = models.TimeField('Activity time', help_text='This is the time of the activity.')
