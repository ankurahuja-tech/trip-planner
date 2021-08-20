from django.urls import path

from .api_views import MarkerViewSet
from .views import MarkerCreateView, MarkerDeleteView, MarkerListView, MarkerUpdateView

app_name = "markers"
urlpatterns = [
    path("trips/<int:trip_pk>/", MarkerListView.as_view(), name="marker_list"),
    path("trips/<int:trip_pk>/create/", MarkerCreateView.as_view(), name="marker_create"),
    # HACK, XXX below: hardcored into "layer.bindPopup" in "markers/marker_list.html" template
    path("trips/<int:trip_pk>/update/<int:pk>/", MarkerUpdateView.as_view(), name="marker_update"),
    # HACK, XXX below: hardcored into "layer.bindPopup" in "markers/marker_list.html" template
    path("trips/<int:trip_pk>/delete/<int:pk>/", MarkerDeleteView.as_view(), name="marker_delete"),
    path("api/trips/<int:trip_pk>/", MarkerViewSet.as_view({"get": "list"}), name="api_trip_markers"),
]
