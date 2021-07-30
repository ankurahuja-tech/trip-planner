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
    # TripDayListView,
    # TripDayDetailView,
    # TripDayCreateView,
    # TripDayUpdateView,
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
    # path('', TripDayListView.as_view(), name='trip_day_list'),
    # path('<int:pk>/', TripDayDetailView.as_view(), name='trip_day_detail'),
    # path('create/', TripDayCreateView.as_view(), name='trip_day_create'),
    # path('<int:pk>/update/', TripDayUpdateView.as_view(), name='trip_day_update'),
]
