from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views.generic.list import ListView

from trip_planner.trips.models import Activity, Trip, TripDay


class CalendarView(LoginRequiredMixin, ListView):
    template_name = "calendars/calendar.html"
    model = Trip

    def get_queryset(self, *args, **kwargs):
        """
        Before returning queryset, prefetches Trip Days and Activities for user's Trips.
        """
        prefetched_data = Prefetch(
            "trip_days",
            queryset=TripDay.objects.order_by("date").prefetch_related(
                Prefetch("activities", queryset=Activity.objects.order_by("time"), to_attr="prefetched_activities")
            ),
            to_attr="prefetched_trip_days",
        )
        qs = super().get_queryset(*args, **kwargs).filter(user=self.request.user).prefetch_related(prefetched_data)
        return qs
