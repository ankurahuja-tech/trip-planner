import datetime

import pytest
from django.urls import resolve, reverse

from config.settings.base import AUTH_USER_MODEL
from trip_planner.trips.models import Activity, Trip, TripDay
from trip_planner.trips.views import TripDayDetailView, TripDetailView, TripListView

# pytestmark = pytest.mark.django_db


# ==============================================================================
# TRIP VIEWS TESTS
# ==============================================================================

# Trip List View tests


def test_trip_list_url_dispatcher(client, user: AUTH_USER_MODEL) -> None:
    response = client.get(reverse("trips:trip_list"))
    trip_list_view_template_name = "trips/trip_list.html"

    assert response.status_code == 200
    assert trip_list_view_template_name in response.template_name


def test_trip_list_url(client, user: AUTH_USER_MODEL) -> None:
    response = client.get("/trips/")

    assert response.status_code == 200


def test_trip_list_url_resolves_triplistview(client) -> None:
    view = resolve("/trips/")

    assert view.func.__name__ == TripListView.as_view().__name__


# Trip Detail View


def test_trip_detail_url_dispatcher(client, trip: Trip) -> None:
    params = {"pk": str(trip.pk)}
    response = client.get(reverse("trips:trip_detail", kwargs=params))
    trip_detail_view_template_name = "trips/trip_detail.html"

    assert response.status_code == 200
    assert trip_detail_view_template_name in response.template_name


def test_trip_detail_url(client, trip: Trip) -> None:
    trip_pk = str(trip.pk)
    response = client.get("/trips/" + trip_pk + "/")

    assert response.status_code == 200


def test_trip_detail_url_resolves_trip_detail_view(client, trip: Trip) -> None:
    trip_pk = str(trip.pk)
    view = resolve("/trips/" + trip_pk + "/")

    assert view.func.__name__ == TripDetailView.as_view().__name__


def test_trip_detail_permission_restriction_wrong_user(client, trip: Trip, wrong_user: AUTH_USER_MODEL) -> None:
    params = {"pk": str(trip.pk)}
    response = client.get(reverse("trips:trip_detail", kwargs=params))

    assert response.status_code == 403


# Trip Create View tests


def test_trip_create(client, user: AUTH_USER_MODEL) -> None:
    context = {
        "title": "New test trip",
        "start_date": "2021-01-01",
        "end_date": "2021-01-03",
        "notes": "Test notes",
    }
    response = client.post(reverse("trips:trip_create"), data=context)
    new_trip = Trip.objects.get(title="New test trip")

    assert response.status_code == 302
    assert new_trip.notes == "Test notes"
    assert new_trip.user == user
    

# Trip Update View tests


def test_trip_update(client, trip: Trip) -> None:
    params = {"pk": trip.pk}
    context = {
        "title": "Updated test trip",
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "notes": trip.notes,
    }
    response = client.post(reverse("trips:trip_update", kwargs=params), data=context)
    trip.refresh_from_db()

    assert response.status_code == 302
    assert trip.title == "Updated test trip"


def test_trip_update_permission_restriction_wrong_user(client, trip: Trip, wrong_user: AUTH_USER_MODEL) -> None:
    params = {"pk": str(trip.pk)}
    response = client.get(reverse("trips:trip_update", kwargs=params))

    assert response.status_code == 403


# Trip Delete View tests


def test_trip_delete(client, trip: Trip) -> None:
    params = {"pk": trip.pk}
    response = client.post(reverse("trips:trip_delete", kwargs=params))

    assert response.status_code == 302
    with pytest.raises(Trip.DoesNotExist):
        assert Trip.objects.get(title="Test trip")


def test_trip_delete_permission_restriction_wrong_user(client, trip: Trip, wrong_user: AUTH_USER_MODEL) -> None:
    params = {"pk": str(trip.pk)}
    response = client.get(reverse("trips:trip_delete", kwargs=params))

    assert response.status_code == 403


# ==============================================================================
# TRIP DAY VIEWS TESTS
# ==============================================================================

# TripDay Detail View tests


def test_trip_day_detail_url_dispatcher(client, trip_day: TripDay) -> None:
    params = {"pk": str(trip_day.pk)}
    response = client.get(reverse("trips:trip_day_detail", kwargs=params))
    trip_day_detail_view_template_name = "trips/trip_day_detail.html"

    assert response.status_code == 200
    assert trip_day_detail_view_template_name in response.template_name


def test_trip_day_detail_url(client, trip_day: TripDay) -> None:
    trip_day_pk = str(trip_day.pk)
    response = client.get("/trips/days/" + trip_day_pk + "/")

    assert response.status_code == 200


def test_trip_day_detail_url_resolves_trip_day_detail_view(client, trip_day: TripDay) -> None:
    trip_day_pk = str(trip_day.pk)
    view = resolve("/trips/days/" + trip_day_pk + "/")

    assert view.func.__name__ == TripDayDetailView.as_view().__name__


def test_trip_day_detail_permission_restriction_wrong_user(
    client, trip_day: TripDay, wrong_user: AUTH_USER_MODEL
) -> None:
    params = {"pk": str(trip_day.pk)}
    response = client.get(reverse("trips:trip_day_detail", kwargs=params))

    assert response.status_code == 403


# TripDay Update View tests


def test_trip_day_update(client, trip_day: TripDay) -> None:
    params = {"pk": trip_day.pk}
    context = {
        "notes": "These are updated notes.",
    }
    response = client.post(reverse("trips:trip_day_update", kwargs=params), data=context)
    trip_day.refresh_from_db()

    assert response.status_code == 302
    assert trip_day.notes == "These are updated notes."


def test_trip_day_update_permission_restriction_wrong_user(
    client, trip_day: TripDay, wrong_user: AUTH_USER_MODEL
) -> None:
    params = {"pk": str(trip_day.pk)}
    response = client.get(reverse("trips:trip_day_update", kwargs=params))

    assert response.status_code == 403


# ==============================================================================
# ACTIVITY TESTS
# ==============================================================================

# Activity Create View tests


def test_activity_create(client, trip_day: TripDay) -> None:
    params = {"pk": trip_day.pk}
    context = {
        "title": "New test activity",
        "time": datetime.time(hour=11, minute=11),
    }
    response = client.post(reverse("trips:activity_create", kwargs=params), data=context)
    new_activity = Activity.objects.get(title="New test activity")

    assert response.status_code == 302
    assert new_activity.day == trip_day


def test_activity_create_permission_restriction_wrong_user(
    client, trip_day: TripDay, wrong_user: AUTH_USER_MODEL
) -> None:
    params = {"pk": str(trip_day.pk)}
    response = client.get(reverse("trips:activity_create", kwargs=params))

    assert response.status_code == 403


# Activity Update View tests


def test_activity_update(client, activity: Activity) -> None:
    params = {
        "trip_day_pk": activity.day.pk,
        "pk": activity.pk,
    }
    context = {
        "title": "These are updated notes.",
        "time": activity.time,
    }
    response = client.post(reverse("trips:activity_update", kwargs=params), data=context)
    activity.refresh_from_db()

    assert response.status_code == 302
    assert activity.title == "These are updated notes."


def test_activity_update_permission_restriction_wrong_user(
    client, activity: Activity, wrong_user: AUTH_USER_MODEL
) -> None:
    params = {
        "trip_day_pk": activity.day.pk,
        "pk": activity.pk,
    }
    response = client.get(reverse("trips:activity_update", kwargs=params))

    assert response.status_code == 403
