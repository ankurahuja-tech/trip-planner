from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Trip

# Create your views here.


class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trip_list'  # this should also work on default as "Trip" is the model name


class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'  # this should also work on default as "Trip" is the model name


class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    fields = [
        'title',
        'start_date',
        'end_date',
        'notes',
    ]
    template_name = 'trips/trip_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TripUpdateView(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = [
        'title',
        'start_date',
        'end_date',
        'notes',
    ]
    template_name = 'trips/trip_update_form.html'
