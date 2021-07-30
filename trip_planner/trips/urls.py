from django.conf.urls import url
from django.urls import path
from .views import TripListView, TripDetailView, TripCreateView, TripUpdateView

app_name = "trips"
urlpatterns = [
    path('', TripListView.as_view(), name='trip_list'),
    path('<int:pk>/', TripDetailView.as_view(), name='trip_detail'),
    path('create/', TripCreateView.as_view(), name='trip_create'),
    path('<int:pk>/update/', TripUpdateView.as_view(), name='trip_update'),
]
