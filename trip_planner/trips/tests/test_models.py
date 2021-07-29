import pytest
import datetime

from config.settings.base import AUTH_USER_MODEL
from trip_planner.trips.models import Trip, TripDay


# ==============================================================================
# FIXTURES
# ==============================================================================

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(django_user_model: AUTH_USER_MODEL) -> AUTH_USER_MODEL:
    user = django_user_model.objects.create_user(username='john', password='testpass123')
    return user


@pytest.fixture
def trip(user: AUTH_USER_MODEL) -> Trip:
    start_date = datetime.date(year=2021, month=7, day=29)
    duration = datetime.timedelta(days=3)
    end_date = start_date + duration
    user = user
    trip = Trip.objects.create(user=user, title='Test trip', start_date=start_date, end_date=end_date)
    return trip


# consider using a mock trip to make it "atomic" from trip TODO
@pytest.fixture
def trip_day(trip: Trip) -> TripDay:
    trip = trip
    date = datetime.date(year=2021, month=7, day=30)
    trip_day = TripDay.objects.create(trip=trip, date=date)
    return trip_day


# ==============================================================================
# TRIP TESTS
# ==============================================================================


def test_trip_exists(trip: Trip) -> None:
    assert Trip.objects.all().count() == 1


def test_trip_fields(trip: Trip) -> None:
    assert trip.user.username == 'john'
    assert trip.title == 'Test trip'
    assert str(trip.start_date) == "2021-07-29"
    assert str(trip.end_date) == "2021-08-01"
    assert trip.notes == ''


def test_trip_str(trip: Trip) -> None:
    assert str(trip) == 'Test trip'


# ==============================================================================
# TRIP DAY TESTS
# ==============================================================================


def test_trip_exists(trip: Trip) -> None:
    assert Trip.objects.all().count() == 1


def test_trip_fields(trip_day: TripDay) -> None:
    assert trip_day.trip.title == 'Test trip'
    assert str(trip_day.date) == "2021-07-30"
    assert trip_day.notes == ''
