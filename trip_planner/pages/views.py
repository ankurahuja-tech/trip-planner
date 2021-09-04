from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import request
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm

# Home Page Views


class HomePageView(TemplateView):
    template_name = "pages/home.html"


# Contact Page Views


class ContactPageView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        """
        Sends email from settings.DEFAULT_FROM_EMAIL to itself with the message provided in the form.
        """
        cleaned_name = form.cleaned_data.get("name")
        cleaned_email = form.cleaned_data.get("email")
        cleaned_subject = form.cleaned_data.get("subject")
        cleaned_message = form.cleaned_data.get("message")

        email_message = f"{cleaned_name} / {cleaned_email} said:"
        email_message += f"\n\nsubject: {cleaned_subject}"
        email_message += f"\n\nmessage: {cleaned_message}"

        send_mail(
            subject=f"Trip Planner: {cleaned_name} / {cleaned_email} said:",
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                settings.DEFAULT_FROM_EMAIL,
            ],
        )

        messages.success(self.request, f"Your message was succesfully sent. Thank you for your input, {cleaned_name}!")

        return super().form_valid(form)
