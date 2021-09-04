from django import forms
from django.forms.widgets import Textarea


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(
        required=False, help_text="(optional) Kindly provide your email to allow me to respond to you."
    )
    subject = forms.CharField(required=True, max_length=75)
    message = forms.CharField(widget=Textarea, required=True, max_length=1200)
