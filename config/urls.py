from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from trip_planner.core.views import ping

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("trip_planner.pages.urls", namespace="pages")),
    path("trips/", include("trip_planner.trips.urls", namespace="trips")),
    path("calendar/", include("trip_planner.calendars.urls", namespace="calendars")),
    path("markers/", include("trip_planner.markers.urls", namespace="markers")),
    path("ping/", ping, name="ping"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django debug_toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
