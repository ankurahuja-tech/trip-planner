from django import forms

from leaflet.forms.widgets import LeafletWidget

from .models import Marker


# Marker Forms


class MarkerCreateForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = (
            'name',
            'geom',
        )
        widgets = {
            'geom': LeafletWidget(),
        }


class MarkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = (
            'name',
            'geom',
        )
        widgets = {
            'geom': LeafletWidget(),
        }
