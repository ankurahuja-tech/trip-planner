import datetime

from trip_planner.trips.views import TripListView, TripDetailView
import pytest
from django.urls import reverse, resolve

from config.settings.base import AUTH_USER_MODEL
from trip_planner.trips.models import Trip, TripDay


# ==============================================================================
# FIXTURES
# ==============================================================================

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(client, django_user_model: AUTH_USER_MODEL) -> AUTH_USER_MODEL:
    user = django_user_model.objects.create_user(username='john', password='testpass123')
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
        user=user, title='Test trip', start_date=start_date, end_date=end_date, notes='Test notes'
    )
    return trip


# ==============================================================================
# TRIP VIEWS TESTS
# ==============================================================================

# Trip List View tests


def test_trip_list_url_status_code_200(client, user: AUTH_USER_MODEL) -> None:
    response = client.get('/trips/')
    assert response.status_code == 200


def test_trip_list_url_dispatcher_status_code_200(client, user: AUTH_USER_MODEL) -> None:
    response = client.get(reverse("trips:trip_list"))
    assert response.status_code == 200


def test_trip_list_template(client, user: AUTH_USER_MODEL):
    response = client.get(reverse("trips:trip_list"))
    trip_list_view_template_name = 'trips/trip_list.html'
    assert trip_list_view_template_name in response.template_name


def test_trip_list_url_resolves_triplistview(client, user: AUTH_USER_MODEL) -> None:
    view = resolve('/trips/')
    assert view.func.__name__ == TripListView.as_view().__name__


# Trip Detail View tests


def test_trip_detail_url_status_code_200(client, user: AUTH_USER_MODEL, trip: Trip) -> None:
    trip_pk = str(trip.pk)
    response = client.get('/trips/' + trip_pk + '/')
    assert response.status_code == 200


def test_trip_detail_url_dispatcher_status_code_200(client, user, trip: Trip) -> None:
    context = {'pk': str(trip.pk)}
    response = client.get(reverse("trips:trip_detail", kwargs=context))
    assert response.status_code == 200


def test_trip_detail_template(client, user: AUTH_USER_MODEL, trip: Trip) -> None:
    trip_pk = {'pk': str(trip.pk)}
    response = client.get(reverse("trips:trip_detail", kwargs=trip_pk))
    trip_detail_view_template_name = 'trips/trip_detail.html'
    assert trip_detail_view_template_name in response.template_name


def test_trip_detail_url_resolves_tripdetailview(client, user: AUTH_USER_MODEL, trip: Trip) -> None:
    trip_pk = str(trip.pk)
    view = resolve('/trips/' + trip_pk + '/')
    assert view.func.__name__ == TripDetailView.as_view().__name__


# Trip Create View tests


def test_trip_create(client, user: AUTH_USER_MODEL) -> None:
    context = {
        'title': 'New test trip',
        'start_date': '2021-01-01',
        'end_date': '2021-01-03',
        'notes': 'Test notes',
    }
    response = client.post(reverse('trips:trip_create'), data=context)
    assert response.status_code == 302

    new_trip = Trip.objects.get(title='New test trip')
    assert new_trip.notes == 'Test notes'


# Trip Update View tests


def test_trip_update(client, trip: Trip) -> None:
    trip_pk = {'pk': trip.id}
    context = {
        'title': 'Updated test trip',
        'start_date': trip.start_date,
        'end_date': trip.end_date,
        'notes': trip.notes,
    }
    response = client.post(reverse('trips:trip_update', kwargs=trip_pk), data=context)
    assert response.status_code == 302

    trip.refresh_from_db()
    assert trip.title == 'Updated test trip'


# Trip Delete View tests


def test_trip_delete(client, trip: Trip) -> None:
    trip_pk = {'pk': trip.id}
    response = client.post(reverse('trips:trip_delete', kwargs=trip_pk))
    assert response.status_code == 302

    # https://stackoverflow.com/questions/3090302/how-do-i-get-the-object-if-it-exists-or-none-if-it-does-not-exist-in-django
    try:
        trip = Trip.objects.get(title='Test trip')
    except Trip.DoesNotExist:
        trip = None
    assert trip == None
