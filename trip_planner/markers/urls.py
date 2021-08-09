from django.conf.urls import url
from django.urls import path
from .views import MarkerListView, MarkerCreateView
from .api_views import MarkerViewSet

app_name = "maps"
urlpatterns = [
    path('trips/<int:trip_pk>/', MarkerListView.as_view(), name='marker_list'),
    path('trips/<int:trip_pk>/create/', MarkerCreateView.as_view(), name='marker_create'),
    path('api/trips/<int:trip_pk>/', MarkerViewSet.as_view({'get': 'list'}), name='api_trip_markers'),
]
