import datetime

import pytest

from trip_planner.trips.models import Activity, Trip, TripDay

# pytestmark = pytest.mark.django_db


# ==============================================================================
# TRIP TESTS
# ==============================================================================

# Generic Trip tests


def test_trip_exists(trip: Trip) -> None:
    assert Trip.objects.all().count() == 1


def test_trip_fields(trip: Trip) -> None:
    assert trip.user.username == "john"
    assert trip.title == "Test trip"
    assert str(trip.start_date) == "2021-07-29"
    assert str(trip.end_date) == "2021-08-01"
    assert trip.notes == "Test notes"


def test_trip_str(trip: Trip) -> None:
    trip.title = "Trip test trip test title"

    assert str(trip) == "Trip test trip test title"


def test_trip_get_absolute_url(trip: Trip) -> None:
    trip_pk = str(trip.pk)

    assert trip.get_absolute_url() == "/trips/" + trip_pk + "/"


# Create TripDays tests


def test_create_trip_days_on_trip_creation(trip: Trip) -> None:
    assert TripDay.objects.all().count() == 4


def test_create_trip_days_on_trip_duration_extension(trip: Trip) -> None:
    trip_duration_factor = datetime.timedelta(days=1)
    trip.end_date += trip_duration_factor
    trip.start_date -= trip_duration_factor
    trip.save(update_fields=["start_date", "end_date"])

    assert TripDay.objects.filter(trip=trip).count() == 6


def test_delete_trip_days_on_trip_duration_reduction(trip: Trip) -> None:
    trip_duration_factor = datetime.timedelta(days=1)
    trip.start_date += trip_duration_factor
    trip.end_date -= trip_duration_factor
    trip.save(update_fields=["start_date", "end_date"])

    assert TripDay.objects.filter(trip=trip).count() == 2


def test_dont_create_trip_days_duplicates_on_trip_update_if_notes_have_changed(trip: Trip) -> None:
    trip_day = TripDay.objects.filter(trip=trip).first()
    trip_day.notes = "updated test trip day note"
    trip_day.save(update_fields=["notes"])
    trip.notes = "updated test trip note"
    trip.save(update_fields=["notes"])

    assert TripDay.objects.filter(trip=trip).count() == 4


def test_trip_day_nums(trip: Trip) -> None:
    trip_first_day = TripDay.objects.get(date=trip.start_date)
    trip_last_day = TripDay.objects.get(date=trip.end_date)

    assert trip_first_day.num == 1
    assert trip_last_day.num == 4


def test_change_trip_day_num_on_start_date_change(trip: Trip) -> None:
    trip.start_date -= datetime.timedelta(days=1)
    trip.save(update_fields=["start_date"])
    trip_new_first_day = TripDay.objects.get(date=trip.start_date)
    trip_last_day = TripDay.objects.get(date=trip.end_date)

    assert trip_new_first_day.num == 1
    assert trip_last_day.num == 5


# ==============================================================================
# TRIP DAY TESTS
# ==============================================================================


def test_trip_day_exists(trip_day: TripDay) -> None:
    expected_date = datetime.date(year=2021, month=1, day=1)

    assert TripDay.objects.filter(date=expected_date).count() == 1


def test_trip_day_fields(trip_day: TripDay) -> None:
    assert trip_day.trip.title == "TripDay test trip"
    assert str(trip_day.date) == "2021-01-01"
    assert trip_day.notes is None


def test_trip_day_str(trip_day: TripDay) -> None:
    assert str(trip_day) == "Day 1"


def test_trip_day_get_absolute_url(trip_day: TripDay) -> None:
    trip_pk = str(trip_day.trip.pk)

    assert trip_day.get_absolute_url() == "/trips/" + trip_pk + "/"


# ==============================================================================
# ACTIVITY TESTS
# ==============================================================================


def test_activity_exists(activity: Activity) -> None:
    expected_title = "Activity test title"

    assert Activity.objects.filter(title=expected_title).count() == 1


def test_activity_str(activity: Activity) -> None:
    assert str(activity) == "Activity test title"


def test_activity_get_absolute_url(activity: Activity) -> None:
    trip_pk = str(activity.trip.pk)

    assert activity.get_absolute_url() == "/trips/" + trip_pk + "/"
