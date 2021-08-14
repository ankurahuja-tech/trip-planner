from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from trip_planner.core.mixins import UserPassesOwnerTestMixin

from .forms import (
    ActivityCreateForm,
    ActivityUpdateForm,
    TripCreateForm,
    TripDayUpdateForm,
    TripUpdateForm,
)
from .models import Activity, Trip, TripDay


# Trip Views


class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = "trips/trip_list.html"
    context_object_name = "trip_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip_list"] = context["trip_list"].filter(user=self.request.user).order_by("start_date")
        return context


class TripDetailView(LoginRequiredMixin, UserPassesOwnerTestMixin, DetailView):
    model = Trip
    template_name = "trips/trip_detail.html"
    context_object_name = "trip"

    def get_queryset(self, *args, **kwargs):
        """
        Before returning queryset, prefetches Trip Days for a given Trip and Activities for these Trip Days.
        """
        prefetched_data = Prefetch(
            "trip_days",
            queryset=TripDay.objects.order_by("date").prefetch_related(
                Prefetch("activities", queryset=Activity.objects.order_by("time"), to_attr="prefetched_activities")
            ),
            to_attr="prefetched_trip_days",
        )
        qs = super().get_queryset(*args, **kwargs).prefetch_related(prefetched_data)
        return qs


class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = "trips/trip_form.html"
    form_class = TripCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TripUpdateView(LoginRequiredMixin, UserPassesOwnerTestMixin, UpdateView):
    model = Trip
    template_name = "trips/trip_update_form.html"
    form_class = TripUpdateForm


class TripDeleteView(LoginRequiredMixin, UserPassesOwnerTestMixin, DeleteView):
    model = Trip
    template_name = "trips/trip_delete.html"
    success_url = reverse_lazy("trips:trip_list")


# TripDay Views


class TripDayUpdateView(LoginRequiredMixin, UserPassesOwnerTestMixin, UpdateView):
    model = TripDay
    template_name = "trips/trip_day_update_form.html"
    form_class = TripDayUpdateForm


# Activity Views


class ActivityCreateView(LoginRequiredMixin, UserPassesOwnerTestMixin, CreateView):
    model = Activity
    template_name = "trips/activity_form.html"
    form_class = ActivityCreateForm
    owner_mixin_model = TripDay  # custom field for UserPassesOwnerTestMixin

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.trip = Trip.objects.get(pk=self.kwargs["trip_pk"])
        form.instance.day = TripDay.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class ActivityUpdateView(LoginRequiredMixin, UserPassesOwnerTestMixin, UpdateView):
    model = Activity
    template_name = "trips/activity_update_form.html"
    form_class = ActivityUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip_pk"] = self.kwargs["trip_pk"]
        context["trip_day_pk"] = self.kwargs["trip_day_pk"]
        return context

    def get_queryset(self, *args, **kwargs):
        trip_day_pk = self.kwargs["trip_day_pk"]
        qs = super().get_queryset(*args, **kwargs).filter(day=trip_day_pk)
        return qs


class ActivityDeleteView(LoginRequiredMixin, UserPassesOwnerTestMixin, DeleteView):
    model = Activity
    template_name = "trips/activity_delete.html"

    def get_success_url(self, **kwargs):
        success_url = reverse_lazy("trips:trip_detail", kwargs={"pk": self.kwargs["trip_pk"]})
        return success_url
