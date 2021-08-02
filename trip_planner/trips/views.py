from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Prefetch

from .models import Trip, TripDay
from .forms import TripCreateForm, TripUpdateForm

# Trip Views


class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trip_list'  # this should also work on default as "Trip" is the model name


class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'  # this should also work on default as "Trip" is the model name

    def get_queryset(self, *args, **kwargs):
        qs = (
            super()
            .get_queryset(*args, **kwargs)
            .prefetch_related(Prefetch('trip_days', queryset=TripDay.objects.order_by('date')))
        )
        return qs


class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trips/trip_form.html'
    form_class = TripCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TripUpdateView(LoginRequiredMixin, UpdateView):
    model = Trip
    template_name = 'trips/trip_update_form.html'
    form_class = TripUpdateForm


class TripDeleteView(LoginRequiredMixin, DeleteView):
    model = Trip
    template_name = 'trips/trip_delete.html'
    success_url = reverse_lazy('trips:trip_list')


# TripDay Views


class TripDayDetailView(DetailView):
    pass


class TripDayUpdateView(UpdateView):
    pass
