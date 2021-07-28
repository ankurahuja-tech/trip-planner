from django.conf import settings
from django.db import models

# Create your models here.

class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Trip title', max_length=255, help_text='This is the title of your trip.')
    start_date = models.DateField('Trip start date', help_text='This is the start date of your trip.')
    end_date = models.DateField('Trip end date', help_text='This is the end date of your trip.')
    notes = models.OneToOneField('Trip notes', help_text='These are your notes regarding the trip.')
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    # consider adding soft delete option TODO
    # is_deleted = models.BooleanField(default=False)
    # deleted_at = models.DateTimeField(null=True, blank=True)


class Day(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Activity(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
