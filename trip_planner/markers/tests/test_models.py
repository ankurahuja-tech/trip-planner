import datetime

import pytest

from config.settings.base import AUTH_USER_MODEL

from trip_planner.trips.models import Trip
from trip_planner.markers.models import Marker


# ==============================================================================
# FIXTURES
# ==============================================================================


# pytestmark = pytest.mark.django_db


@pytest.fixture
def user(client, django_user_model: AUTH_USER_MODEL) -> AUTH_USER_MODEL:
    user = django_user_model.objects.create_user(username="john", password="testpass123")
    client.force_login(user)
    return user


@pytest.fixture
def trip(user: AUTH_USER_MODEL) -> Trip:
    """
    Creates test trip with 4 trip days fixture.
    """
    start_date = datetime.date(year=2021, month=7, day=29)
    duration = datetime.timedelta(days=3)
    end_date = start_date + duration
    user = user
    trip = Trip.objects.create(
        user=user, title="Test trip", start_date=start_date, end_date=end_date, notes="Test notes"
    )
    return trip


@pytest.fixture
def marker(trip: Trip) -> Marker:
    """
    Creates test marker.
    """
    marker = Marker.objects.create(
        user=trip.user, trip=trip, name="New test marker", geom='{"type": "Point", "coordinates": [21.599464, 53.981935]}',
    )
    return marker


# ==============================================================================
# MARKER TESTS
# ==============================================================================


# Generic Marker tests


def test_marker_get_absolute_url(marker: Marker) -> None:
    trip_pk = str(marker.trip.pk)

    assert marker.get_absolute_url() == "/markers/trips/" + trip_pk + "/"
