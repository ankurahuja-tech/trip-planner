from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Prefetch

from .models import Trip, TripDay, Activity
from .forms import TripCreateForm, TripDayUpdateForm, TripUpdateForm, ActivityCreateForm, ActivityUpdateForm


# Trip Views


class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trip_list'


class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'

    def get_queryset(self, *args, **kwargs):
        prefetch_trip_days = Prefetch('trip_days', queryset=TripDay.objects.order_by('date'))
        qs = super().get_queryset(*args, **kwargs).prefetch_related(prefetch_trip_days)
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


class TripDayDetailView(LoginRequiredMixin, DetailView):
    model = TripDay
    template_name = 'trips/trip_day_detail.html'
    context_object_name = 'trip_day'

    def get_queryset(self, *args, **kwargs):
        prefetch_activities = Prefetch('activities', queryset=Activity.objects.order_by('time'))
        qs = super().get_queryset(*args, **kwargs).prefetch_related(prefetch_activities)
        return qs


class TripDayUpdateView(LoginRequiredMixin, UpdateView):
    model = TripDay
    template_name = 'trips/trip_day_update_form.html'
    form_class = TripDayUpdateForm


# Activity Views


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'trips/activity_form.html'
    form_class = ActivityCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.day = TripDay.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    template_name = 'trips/activity_update_form.html'
    form_class = ActivityUpdateForm
