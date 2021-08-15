import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from trip_planner.core.models import TimeStampedModel


# Trip


def user_directory_path(instance, filename):
    """ Sets path to user uploads to: MEDIA_ROOT/user_<id>/<filename> """
    return f'user_{instance.user.id}/{filename}'


class Trip(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("Trip title", max_length=50, help_text="This is the title of your trip.")
    start_date = models.DateField("Trip start date", help_text="This is the start date of your trip.")
    end_date = models.DateField("Trip end date", help_text="This is the end date of your trip.")
    # TODO: description = models.CharField("Trip description", help_text="This is a short description of the trip.", blank=True, null=True)
    notes = models.TextField("Trip notes", help_text="These are your notes regarding the trip.", blank=True, null=True)
    picture = ProcessedImageField(upload_to=user_directory_path, processors=[Thumbnail(width=600, height=400, upscale=True)], format='JPEG', options={'quality': 80}, blank=True, help_text="This is the 3:2 ratio picture associated with the trip.")
    # TODO: location
    # NOTE: consider: past/ongoing/future choices
    # NOTE: consider: budget field / app

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("trips:trip_detail", kwargs={"pk": self.pk})

    def create_trip_days(self):
        """
        Creates trip days for a new or updated Trip instance, provided that they are not already created.
        """
        trip_duration = self.end_date - self.start_date

        # get list of dates for the Trip
        trip_dates = []
        for date in range(trip_duration.days + 1):
            trip_date = self.start_date + datetime.timedelta(days=date)
            trip_dates.append(trip_date)

        # create TripDay instance for each day of the Trip
        for trip_date in trip_dates:
            TripDay.objects.get_or_create(user=self.user, trip=self, date=trip_date)

    def update_trip_days_nums(self):
        """
        Update TripDay object's "num" field for each TripDay object a particular Trip.
        """
        # get and order list of TripDays for the Trip
        trip_days = TripDay.objects.all().filter(trip=self).order_by("date")

        # update TripDays "num" fields
        num_increment = 1
        for trip_day in trip_days:
            if trip_day.num != num_increment:
                trip_day.num = num_increment
                trip_day.save(update_fields=["num"])
            num_increment += 1

    def delete_extra_trip_days(self):
        """
        Delete extra TripDay objects if there are more than Trip's duration.
        """
        # get list of dates in the Trip
        trip_duration = (self.end_date - self.start_date).days
        trip_dates = [self.start_date + datetime.timedelta(days=date) for date in range(trip_duration + 1)]

        # get list of TripDays for the Trip
        trip_days = TripDay.objects.all().filter(trip=self)

        # delete TripDays that are not in Trip's list of dates
        for trip_day in trip_days:
            if trip_day.date not in trip_dates:
                TripDay.objects.filter(id=trip_day.id).delete()

    def save(self, *args, **kwargs):
        """
        Save Trip object instance in the database and create TripDay objects for each day of the trip.
        """
        super().save(*args, **kwargs)
        self.create_trip_days()
        self.update_trip_days_nums()
        self.delete_extra_trip_days()


# Trip Day


class TripDay(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_days")
    num = models.IntegerField(
        "day of the trip", help_text="This shows what day of the trip is this.", blank=True, null=True
    )
    date = models.DateField("date", help_text="This is a date within the trip.")
    notes = models.TextField(
        "Day notes", help_text="These are your notes for the day of the trip.", blank=True, null=True
    )

    def __str__(self) -> str:
        return "Day " + str(self.num)

    def get_absolute_url(self):
        return reverse("trips:trip_detail", kwargs={"pk": self.trip.pk})


# Activity


class Activity(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="activities")
    day = models.ForeignKey(TripDay, on_delete=models.CASCADE, related_name="activities")
    title = models.CharField("Activity title", max_length=50, help_text="This is the title of your activity.")
    time = models.TimeField("Activity time", help_text="This is the time of the activity.")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("trips:trip_detail", kwargs={"pk": self.trip.pk})
