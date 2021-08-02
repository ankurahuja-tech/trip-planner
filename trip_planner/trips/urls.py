from django.conf.urls import url
from django.urls import path
from .views import (
    # Trip Views
    TripListView,
    TripDetailView,
    TripCreateView,
    TripUpdateView,
    TripDeleteView,
    # TripDay Views
    TripDayDetailView,
    TripDayUpdateView,
    # Activity Views
    ActivityCreateView,
    ActivityUpdateView,
)

app_name = "trips"
urlpatterns = [
    # Trip urls
    path('', TripListView.as_view(), name='trip_list'),
    path('<int:pk>/', TripDetailView.as_view(), name='trip_detail'),
    path('create/', TripCreateView.as_view(), name='trip_create'),
    path('<int:pk>/update/', TripUpdateView.as_view(), name='trip_update'),
    path('<int:pk>/delete/', TripDeleteView.as_view(), name='trip_delete'),
    # TripDay urls
    path('days/<int:pk>/', TripDayDetailView.as_view(), name='trip_day_detail'),
    path('days/<int:pk>/update/', TripDayUpdateView.as_view(), name='trip_day_update'),
    # Activity urls
    path('days/<int:pk>/add-activity/', ActivityCreateView.as_view(), name='activity_create'),
    path('days/<int:pk>/update-activity/', ActivityUpdateView.as_view(), name='activity_update'),
]
