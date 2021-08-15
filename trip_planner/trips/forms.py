import datetime

from django import forms

from .models import Activity, Trip, TripDay

from crispy_forms.helper import FormHelper

# Custom Widgets


# https://www.youtube.com/watch?v=I2-JYxnSiB0
class CustomDateInput(forms.DateInput):
    """
    Creates a custom widget that changes DateField input to HTML5 "date" field.
    """

    input_type = "date"


class CustomTimeInput(forms.DateInput):
    """
    Creates a custom widget that changes TimeField input to HTML5 "time" field.
    """

    input_type = "time"


# Trip Forms


class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = (
            "title",
            "start_date",
            "end_date",
            "notes",
        )
        widgets = {
            "start_date": CustomDateInput(),
            "end_date": CustomDateInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # asserts that a given Trip's end date does not come before start date
        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', "Trip end date cannot come before Trip start date.")
        
        # asserts that Trip's duration is not longer than 90 days
        max_trip_duration = datetime.timedelta(days=90)
        if (end_date - start_date) > max_trip_duration:
            self.add_error('end_date', "This app version does not support Trip duration exceeding 90 days. Sorry!")
        
        return cleaned_data


class TripUpdateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = (
            "title",
            "start_date",
            "end_date",
            "notes",
        )
        widgets = {
            "start_date": CustomDateInput(),
            "end_date": CustomDateInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # asserts that a given Trip's end date does not come before start date
        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', "Trip end date cannot come before Trip start date.")
        
        # asserts that Trip's duration is not longer than 90 days
        max_trip_duration = datetime.timedelta(days=90)
        if (end_date - start_date) > max_trip_duration:
            self.add_error('end_date', "This app version does not support Trip duration exceeding 90 days. Sorry!")
        
        return cleaned_data


class TripUpdateFormPicture(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ("picture",)


# Trip Day Forms


class TripDayUpdateForm(forms.ModelForm):
    class Meta:
        model = TripDay
        fields = ("notes",)


# Activity Forms


class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            "title",
            "time",
        )
        widgets = {
            "time": CustomTimeInput(),
        }


class ActivityUpdateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            "title",
            "time",
        )
        widgets = {
            "time": CustomTimeInput(),
        }
