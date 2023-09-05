from rest_framework import viewsets

from .models import Marker
from .serializers import MarkerSerializer


class MarkerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Filters queryset by user and trip.
        """
        qs = super().get_queryset(*args, **kwargs).filter(user=self.request.user).filter(trip=self.kwargs["trip_pk"])
        return qs


class MarkerViewSetAllTrips(viewsets.ReadOnlyModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Filters queryset by user.
        """
        qs = super().get_queryset(*args, **kwargs).filter(user=self.request.user)
        return qs
