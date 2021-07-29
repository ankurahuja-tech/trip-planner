import datetime

import pytest

# from unittest.mock import patch, MagicMock

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
    date = datetime.date(year=2021, month=1, day=1)
    trip_day = TripDay.objects.create(trip=trip, date=date)
    return trip_day


# ==============================================================================
# TRIP TESTS
# ==============================================================================


# Generic Trip tests


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


# Create TripDays tests


def test_create_trip_days_on_trip_creation(trip: Trip) -> None:
    assert TripDay.objects.all().count() == 4


def test_create_trip_days_on_trip_duration_extension(trip: Trip) -> None:
    trip_duration_factor = datetime.timedelta(days=1)

    trip.end_date += trip_duration_factor
    trip.save(update_fields=['end_date'])
    assert TripDay.objects.all().count() == 5

    trip.start_date -= trip_duration_factor
    trip.save(update_fields=['start_date'])
    assert TripDay.objects.all().count() == 6


def test_trip_day_num(trip: Trip) -> None:
    trip_first_day = TripDay.objects.get(date=trip.start_date)
    assert trip_first_day.num == 1


# def test_change_trip_day_num_on_start_date_change(trip: Trip) -> None: TODO
#     pass


# ==============================================================================
# TRIP DAY TESTS
# ==============================================================================


def test_trip_day_exists(trip_day: TripDay) -> None:
    expected_date = datetime.date(year=2021, month=1, day=1)
    assert TripDay.objects.filter(date=expected_date).count() == 1


def test_trip_day_fields(trip_day: TripDay) -> None:
    assert trip_day.trip.title == 'Test trip'
    assert str(trip_day.date) == "2021-01-01"
    assert trip_day.notes == ''
