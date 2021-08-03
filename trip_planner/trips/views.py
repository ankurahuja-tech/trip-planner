from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_list'] = context['trip_list'].filter(user=self.request.user)
        return context


class TripDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'

    def test_func(self) -> bool:
        """
        Check if user is the owner of the requested data.
        """
        return self.request.user == Trip.objects.get(pk=self.kwargs['pk']).user

    def get_queryset(self, *args, **kwargs):
        """
        Before returning queryset, prefetches Trip Days for a given Trip and Activities for these Trip Days.
        """
        prefetched_data = Prefetch(
            'trip_days',
            queryset=TripDay.objects.order_by('date').prefetch_related(
                Prefetch('activities', queryset=Activity.objects.order_by('time'), to_attr="prefetched_activities")
            ),
            to_attr="prefetched_trip_days",
        )
        qs = super().get_queryset(*args, **kwargs).prefetch_related(prefetched_data)
        return qs


class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trips/trip_form.html'
    form_class = TripCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TripUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Trip
    template_name = 'trips/trip_update_form.html'
    form_class = TripUpdateForm

    def test_func(self) -> bool:
        """
        Check if user is the owner of the requested data.
        """
        return self.request.user == Trip.objects.get(pk=self.kwargs['pk']).user


class TripDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Trip
    template_name = 'trips/trip_delete.html'
    success_url = reverse_lazy('trips:trip_list')

    def test_func(self) -> bool:
        """
        Check if user is the owner of the requested data.
        """
        return self.request.user == Trip.objects.get(pk=self.kwargs['pk']).user


# TripDay Views


class TripDayDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = TripDay
    template_name = 'trips/trip_day_detail.html'
    context_object_name = 'trip_day'

    def get_queryset(self, *args, **kwargs):
        """
        Before returning queryset, prefetches Activities for a given Trip Day.
        """
        prefetched_data = Prefetch(
            'activities', queryset=Activity.objects.order_by('time'), to_attr="prefetched_activities"
        )
        qs = super().get_queryset(*args, **kwargs).prefetch_related(prefetched_data)
        return qs

    def test_func(self) -> bool:
        """
        Check if user is the owner of the requested data.
        """
        return self.request.user == TripDay.objects.get(pk=self.kwargs['pk']).user


class TripDayUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TripDay
    template_name = 'trips/trip_day_update_form.html'
    form_class = TripDayUpdateForm

    def test_func(self) -> bool:
        """
        Check if user is the owner of the requested data.
        """
        return self.request.user == TripDay.objects.get(pk=self.kwargs['pk']).user


# Activity Views


class ActivityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Activity
    template_name = 'trips/activity_form.html'
    form_class = ActivityCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.day = TripDay.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self) -> bool:
        """
        Check if user is the owner of the requested data.
        """
        return self.request.user == TripDay.objects.get(pk=self.kwargs['pk']).user


class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Activity
    template_name = 'trips/activity_update_form.html'
    form_class = ActivityUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_day_pk'] = self.kwargs['trip_day_pk']
        return context

    def get_queryset(self, *args, **kwargs):
        trip_day_pk = self.kwargs['trip_day_pk']
        qs = super().get_queryset(*args, **kwargs).filter(day=trip_day_pk)
        return qs

    def test_func(self) -> bool:
        """
        Check if user is the owner of the requested data.
        """
        return self.request.user == Activity.objects.get(pk=self.kwargs['pk']).user
