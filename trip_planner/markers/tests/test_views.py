import datetime

import pytest
from django.urls import resolve, reverse

from config.settings.base import AUTH_USER_MODEL
from trip_planner.markers.models import Marker
from trip_planner.markers.views import MarkerListView, MarkerListViewAllTrips
from trip_planner.trips.models import Trip

# ==============================================================================
# FIXTURES
# ==============================================================================


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


# ==============================================================================
# MARKER VIEW TESTS
# ==============================================================================


# Marker List View tests


def test_marker_list_url_dispatcher(client, trip: Trip) -> None:
    params = {"trip_pk": str(trip.pk)}
    response = client.get(reverse("markers:marker_list", kwargs=params))
    marker_list_view_template_name = "markers/marker_list.html"

    assert response.status_code == 200
    assert marker_list_view_template_name in response.template_name


def test_marker_list_url(client, trip: Trip) -> None:
    trip_pk = str(trip.pk)
    response = client.get("/markers/trips/" + trip_pk + "/")

    assert response.status_code == 200


def test_marker_list_url_resolves_marker_list_view(client, trip: Trip) -> None:
    trip_pk = str(trip.pk)
    view = resolve("/markers/trips/" + trip_pk + "/")

    assert view.func.__name__ == MarkerListView.as_view().__name__


def test_marker_list_permission_restriction_wrong_user(client, trip: Trip, wrong_user: AUTH_USER_MODEL) -> None:
    params = {"trip_pk": str(trip.pk)}
    response = client.get(reverse("markers:marker_list", kwargs=params))

    assert response.status_code == 403


# Marker Create View


def test_marker_create(client, trip: Trip) -> None:
    params = {"trip_pk": trip.pk}
    context = {
        "user": trip.user,
        "trip": trip,
        "name": "New test marker",
        "geom": '{"type": "Point", "coordinates": [21.599464, 53.981935]}',
    }
    response = client.post(reverse("markers:marker_create", kwargs=params), data=context)
    new_marker = Marker.objects.get(name="New test marker")

    assert response.status_code == 302
    assert new_marker.trip == trip


def test_marker_create_permission_restriction_wrong_user(client, trip: Trip, wrong_user: AUTH_USER_MODEL) -> None:
    params = {"trip_pk": str(trip.pk)}
    response = client.get(reverse("markers:marker_create", kwargs=params))

    assert response.status_code == 403


# Marker List All Trips View tests


def test_marker_list_all_trips_url_dispatcher(client, user: AUTH_USER_MODEL) -> None:
    response = client.get(reverse("markers:marker_list_all_trips"))
    marker_list_all_trips_view_template_name = "markers/marker_list_all_trips.html"

    assert response.status_code == 200
    assert marker_list_all_trips_view_template_name in response.template_name


def test_marker_list_all_trips_url(client, user: AUTH_USER_MODEL) -> None:
    response = client.get("/markers/trips/")

    assert response.status_code == 200


def test_marker_list_all_trips_url_resolves_marker_list_view(client, user: AUTH_USER_MODEL) -> None:
    view = resolve("/markers/trips/")

    assert view.func.__name__ == MarkerListViewAllTrips.as_view().__name__


# Tests for when user is notlogged in


def test_marker_list_all_trips_not_logged_in_status_code_302(client):
    response = client.get(reverse("markers:marker_list_all_trips"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_marker_list_all_trips_not_logged_in_redirect_to_login(client):
    response = client.get(reverse("markers:marker_list_all_trips"))
    redirected_login_url = (
        "/accounts/login/?next=/markers/trips/"  # equivalent to django settings.LOGIN_URL + "?next=/"
    )
    assert response.url == redirected_login_url
