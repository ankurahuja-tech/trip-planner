import pytest

from config.settings.base import AUTH_USER_MODEL
from trip_planner.trips.forms import TripCreateForm, TripUpdateForm
from trip_planner.trips.models import Trip

# pytestmark = pytest.mark.django_db


# ==============================================================================
# TRIP FORMS TESTS
# ==============================================================================

# Trip Create Form tests


def test_trip_create_form_valid(client, user: AUTH_USER_MODEL) -> None:
    submitted_data = {
        "title": "New test trip",
        "start_date": "2021-01-01",
        "end_date": "2021-01-03",
        "notes": "Test notes",
    }
    form = TripCreateForm(data=submitted_data)

    assert not form.errors


def test_trip_create_form_end_date_before_start_date_invalid(client, user: AUTH_USER_MODEL) -> None:
    submitted_data = {
        "title": "New test trip",
        "start_date": "2021-01-03",
        "end_date": "2021-01-01",
        "notes": "Test notes",
    }
    form = TripCreateForm(data=submitted_data)

    assert form.errors["end_date"] == ["Trip end date cannot come before Trip start date."]


def test_trip_create_form_trip_duration_invalid(client, user: AUTH_USER_MODEL) -> None:
    submitted_data = {
        "title": "New test trip",
        "start_date": "2021-01-01",
        "end_date": "2021-04-02",
        "notes": "Test notes",
    }
    form = TripCreateForm(data=submitted_data)

    assert form.errors["end_date"] == ["This app version does not support Trip duration exceeding 90 days. Sorry!"]


# Trip Update Form tests


def test_trip_update_form_valid(client, trip: Trip) -> None:
    submitted_data = {
        "title": "New test trip",
        "start_date": "2021-01-01",
        "end_date": "2021-01-03",
        "notes": "Test notes",
    }
    form = TripUpdateForm(data=submitted_data)

    assert not form.errors


def test_trip_update_form_end_date_before_start_date_invalid(client, trip: Trip) -> None:
    submitted_data = {
        "title": "Test trip",
        "start_date": "2021-07-29",
        "end_date": "2021-07-28",
        "notes": "Test notes",
    }
    form = TripUpdateForm(data=submitted_data)

    assert form.errors["end_date"] == ["Trip end date cannot come before Trip start date."]


def test_trip_update_form_trip_duration_invalid(client, trip: Trip) -> None:
    submitted_data = {
        "title": "Test trip",
        "start_date": "2021-07-29",
        "end_date": "2021-11-29",
        "notes": "Test notes",
    }
    form = TripUpdateForm(data=submitted_data)

    assert form.errors["end_date"] == ["This app version does not support Trip duration exceeding 90 days. Sorry!"]
