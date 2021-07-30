import datetime

import pytest

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
    """
    Creates test trip with 4 trip days fixture.
    """
    start_date = datetime.date(year=2021, month=7, day=29)
    duration = datetime.timedelta(days=3)
    end_date = start_date + duration
    user = user
    trip = Trip.objects.create(user=user, title='Trip test trip', start_date=start_date, end_date=end_date)
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
    trip = Trip.objects.create(user=user, title='TripDay test trip', start_date=start_date, end_date=end_date)

    # Get TripDay object
    trip_day = TripDay.objects.get(trip=trip)
    return trip_day


# ==============================================================================
# TRIP TESTS
# ==============================================================================


# Generic Trip tests


def test_trip_exists(trip: Trip) -> None:
    assert Trip.objects.all().count() == 1


def test_trip_fields(trip: Trip) -> None:
    assert trip.user.username == 'john'
    assert trip.title == 'Trip test trip'
    assert str(trip.start_date) == "2021-07-29"
    assert str(trip.end_date) == "2021-08-01"
    assert trip.notes == ''


def test_trip_str(trip: Trip) -> None:
    trip.title = 'Trip test trip test title'
    assert str(trip) == 'Trip test trip test title'


def test_get_absolute_url(trip: Trip) -> None:
    trip_pk = str(trip.pk)
    assert trip.get_absolute_url() == '/trips/' + trip_pk + '/'


# Create TripDays tests


def test_create_trip_days_on_trip_creation(trip: Trip) -> None:
    assert TripDay.objects.all().count() == 4


def test_create_trip_days_on_trip_duration_extension(trip: Trip) -> None:
    trip_duration_factor = datetime.timedelta(days=1)

    trip.end_date += trip_duration_factor
    trip.save(update_fields=['end_date'])
    assert TripDay.objects.filter(trip=trip).count() == 5

    trip.start_date -= trip_duration_factor
    trip.save(update_fields=['start_date'])
    assert TripDay.objects.filter(trip=trip).count() == 6


def test_dont_create_trip_days_duplicates_on_trip_update_if_trip_day_notes_have_changed(trip: Trip) -> None:
    trip_day = TripDay.objects.filter(trip=trip).first()
    trip_day.notes = 'test note'
    trip_day.save(update_fields=['notes'])

    trip.notes = 'test note'
    trip.save(update_fields=['notes'])

    assert TripDay.objects.filter(trip=trip).count() == 4


def test_trip_day_nums(trip: Trip) -> None:
    trip_first_day = TripDay.objects.get(date=trip.start_date)
    assert trip_first_day.num == 1

    trip_last_day = TripDay.objects.get(date=trip.end_date)
    assert trip_last_day.num == 4


def test_change_trip_day_num_on_start_date_change(trip: Trip) -> None:
    trip.start_date -= datetime.timedelta(days=1)
    trip.save(update_fields=['start_date'])

    trip_new_first_day = TripDay.objects.get(date=trip.start_date)
    assert trip_new_first_day.num == 1

    trip_last_day = TripDay.objects.get(date=trip.end_date)
    assert trip_last_day.num == 5


# ==============================================================================
# TRIP DAY TESTS
# ==============================================================================


def test_trip_day_exists(trip_day: TripDay) -> None:
    expected_date = datetime.date(year=2021, month=1, day=1)
    assert TripDay.objects.filter(date=expected_date).count() == 1


def test_trip_day_fields(trip_day: TripDay) -> None:
    assert trip_day.trip.title == 'TripDay test trip'
    assert str(trip_day.date) == "2021-01-01"
    assert trip_day.notes == ''


def test_trip_day_str(trip_day: TripDay) -> None:
    assert str(trip_day) == 'Day 1'


# TODO
# def test_get_absolute_url(trip_day: TripDay) -> None:
#     trip_pk = str(trip_day.trip)
#     trip_day_pk = str(trip_day.pk)
#     assert trip.get_absolute_url() == '/trips/' + trip_pk + '/days/' + trip_day_pk + '/'
