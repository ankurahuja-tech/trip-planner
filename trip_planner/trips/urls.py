from django.urls import path

from .views import (  # Trip Views; TripDay Views; Activity Views
    ActivityCreateView,
    ActivityDeleteView,
    ActivityUpdateView,
    TripCreateView,
    TripDayDetailView,
    TripDayUpdateView,
    TripDeleteView,
    TripDetailView,
    TripListView,
    TripUpdateView,
)

app_name = "trips"
urlpatterns = [
    # Trip urls
    path("", TripListView.as_view(), name="trip_list"),
    path("create/", TripCreateView.as_view(), name="trip_create"),
    path("<int:pk>/", TripDetailView.as_view(), name="trip_detail"),
    path("<int:pk>/update/", TripUpdateView.as_view(), name="trip_update"),
    path("<int:pk>/delete/", TripDeleteView.as_view(), name="trip_delete"),
    # TripDay urls
    path("days/<int:pk>/", TripDayDetailView.as_view(), name="trip_day_detail"), # TODO: remove!
    path("days/<int:pk>/update/", TripDayUpdateView.as_view(), name="trip_day_update"), # TODO: remove!
    # Activity urls
    path("days/<int:pk>/add-activity/", ActivityCreateView.as_view(), name="activity_create"), # TODO add trip here and to model
    path("days/<int:trip_day_pk>/update-activity/<int:pk>", ActivityUpdateView.as_view(), name="activity_update"), # TODO add trip here and to model
    path("<int:trip_pk>/days/<int:trip_day_pk>/delete-activity/<int:pk>", ActivityDeleteView.as_view(), name="activity_delete"),
]
