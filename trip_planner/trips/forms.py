from django import forms

from .models import Trip

# https://www.youtube.com/watch?v=I2-JYxnSiB0
class CustomDateInput(forms.DateInput):
    """
    Creates a custom widget that changes DateField input to HTML5 "date" field.
    """

    input_type = 'date'


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
