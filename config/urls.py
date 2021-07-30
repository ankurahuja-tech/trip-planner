from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('trip_planner.accounts.urls', namespace='accounts')),
    path('', include('trip_planner.pages.urls', namespace='pages')),
    path('calendar/', include('trip_planner.calendars.urls', namespace='calendars')),
    path('trips/', include('trip_planner.trips.urls', namespace='trips')),
]

# Django debug_toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
