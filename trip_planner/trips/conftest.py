import datetime

import pytest

from config.settings.base import AUTH_USER_MODEL
from trip_planner.trips.models import Activity, Trip, TripDay

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
def wrong_user(client, django_user_model: AUTH_USER_MODEL) -> AUTH_USER_MODEL:
    wrong_user = django_user_model.objects.create_user(username="johnny", password="testpass123")
    client.force_login(wrong_user)
    return wrong_user


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


# consider using a mock trip to avoid accessing the db TODO
@pytest.fixture
def trip_day(user: AUTH_USER_MODEL) -> TripDay:
    """
    Creates a trip day fixture for TripDay tests.
    """
    # Create Trip object
    start_date = datetime.date(year=2021, month=1, day=1)
    end_date = start_date
    user = user
    trip = Trip.objects.create(user=user, title="TripDay test trip", start_date=start_date, end_date=end_date)

    # Get TripDay object
    trip_day = TripDay.objects.get(trip=trip)
    return trip_day


@pytest.fixture
def activity(trip_day: TripDay) -> Activity:
    """
    Creates an activity fixture for a trip day.
    """
    # Create Activity object
    user = trip_day.user
    day = trip_day
    activity = Activity.objects.create(
        user=user, day=day, title="Activity test title", time=datetime.time(hour=11, minute=11)
    )
    return activity
