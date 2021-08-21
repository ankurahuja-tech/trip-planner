from django.urls import path

from .views import (  # Trip Views; TripDay Views; Activity Views
    ActivityCreateView,
    ActivityDeleteView,
    ActivityUpdateView,
    TripCreateView,
    TripDayUpdateView,
    TripDeleteView,
    TripDetailView,
    TripListView,
    TripUpdateView,
    TripUpdateViewPicture,
)

app_name = "trips"
urlpatterns = [
    # Trip urls
    path("", TripListView.as_view(), name="trip_list"),
    path("create/", TripCreateView.as_view(), name="trip_create"),
    path("<int:pk>/", TripDetailView.as_view(), name="trip_detail"),
    path("<int:pk>/update/", TripUpdateView.as_view(), name="trip_update"),
    path("<int:pk>/delete/", TripDeleteView.as_view(), name="trip_delete"),
    path("<int:pk>/picture-update/", TripUpdateViewPicture.as_view(), name="trip_update_picture"),
    # TripDay urls
    path("<int:trip_pk>/days/<int:pk>/update/", TripDayUpdateView.as_view(), name="trip_day_update"),
    # Activity urls
    path("<int:trip_pk>/days/<int:pk>/add-activity/", ActivityCreateView.as_view(), name="activity_create"),
    path(
        "<int:trip_pk>/days/<int:trip_day_pk>/activities/<int:pk>/update/",
        ActivityUpdateView.as_view(),
        name="activity_update",
    ),
    path(
        "<int:trip_pk>/days/<int:trip_day_pk>/activities/<int:pk>/delete/",
        ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
]
