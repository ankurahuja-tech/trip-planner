from django import forms

from .models import Trip, TripDay, Activity


# Custom Widgets


# https://www.youtube.com/watch?v=I2-JYxnSiB0
class CustomDateInput(forms.DateInput):
    """
    Creates a custom widget that changes DateField input to HTML5 "date" field.
    """

    input_type = 'date'


class CustomTimeInput(forms.DateInput):
    """
    Creates a custom widget that changes TimeField input to HTML5 "time" field.
    """

    input_type = 'time'


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
            'start_date': CustomDateInput(),
            'end_date': CustomDateInput(),
        }


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
            'start_date': CustomDateInput(),
            'end_date': CustomDateInput(),
        }


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
            'time': CustomTimeInput(),
        }


class ActivityUpdateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            "title",
            "time",
        )
        widgets = {
            'time': CustomTimeInput(),
        }
