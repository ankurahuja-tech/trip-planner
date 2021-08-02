import datetime

from trip_planner.trips.views import TripListView, TripDetailView, TripDayDetailView
import pytest
from django.urls import reverse, resolve

from config.settings.base import AUTH_USER_MODEL
from trip_planner.trips.models import Activity, Trip, TripDay


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


@pytest.fixture
def activity(trip_day: TripDay) -> Activity:
    """
    Creates an activity fixture for a trip day.
    """
    # Create Activity object
    user = trip_day.user
    day = trip_day
    activity = Activity.objects.create(user=user, day=day, title='Activity test title', time=datetime.time(hour=11, minute=11))
    return activity


# ==============================================================================
# TRIP VIEWS TESTS
# ==============================================================================

# Trip List View tests


def test_trip_list_url_dispatcher(client, user: AUTH_USER_MODEL) -> None:
    response = client.get(reverse("trips:trip_list"))
    trip_list_view_template_name = 'trips/trip_list.html'

    assert response.status_code == 200
    assert trip_list_view_template_name in response.template_name


def test_trip_list_url(client, user: AUTH_USER_MODEL) -> None:
    response = client.get('/trips/')

    assert response.status_code == 200


def test_trip_list_url_resolves_triplistview(client) -> None:
    view = resolve('/trips/')

    assert view.func.__name__ == TripListView.as_view().__name__


# Trip Detail View


def test_trip_detail_url_dispatcher(client, trip: Trip) -> None:
    trip_pk = {'pk': str(trip.pk)}
    response = client.get(reverse("trips:trip_detail", kwargs=trip_pk))
    trip_detail_view_template_name = 'trips/trip_detail.html'

    assert response.status_code == 200
    assert trip_detail_view_template_name in response.template_name


def test_trip_detail_url(client, trip: Trip) -> None:
    trip_pk = str(trip.pk)
    response = client.get('/trips/' + trip_pk + '/')

    assert response.status_code == 200


def test_trip_detail_url_resolves_trip_detail_view(client, trip: Trip) -> None:
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
    new_trip = Trip.objects.get(title='New test trip')

    assert response.status_code == 302
    assert new_trip.notes == 'Test notes'
    assert new_trip.user == user


# Trip Update View tests


def test_trip_update(client, trip: Trip) -> None:
    trip_pk = {'pk': trip.pk}
    context = {
        'title': 'Updated test trip',
        'start_date': trip.start_date,
        'end_date': trip.end_date,
        'notes': trip.notes,
    }
    response = client.post(reverse('trips:trip_update', kwargs=trip_pk), data=context)
    trip.refresh_from_db()

    assert response.status_code == 302
    assert trip.title == 'Updated test trip'


# Trip Delete View tests


def test_trip_delete(client, trip: Trip) -> None:
    trip_pk = {'pk': trip.pk}
    response = client.post(reverse('trips:trip_delete', kwargs=trip_pk))

    assert response.status_code == 302
    with pytest.raises(Trip.DoesNotExist):
        assert Trip.objects.get(title='Test trip')


# ==============================================================================
# TRIP DAY VIEWS TESTS
# ==============================================================================

# TripDay Detail View tests


def test_trip_day_detail_url_dispatcher(client, trip_day: TripDay) -> None:
    trip_day_pk = {'pk': str(trip_day.pk)}
    response = client.get(reverse("trips:trip_day_detail", kwargs=trip_day_pk))
    trip_day_detail_view_template_name = 'trips/trip_day_detail.html'

    assert response.status_code == 200
    assert trip_day_detail_view_template_name in response.template_name


def test_trip_day_detail_url(client, trip_day: TripDay) -> None:
    trip_day_pk = str(trip_day.pk)
    response = client.get('/trips/days/' + trip_day_pk + '/')

    assert response.status_code == 200


def test_trip_day_detail_url_resolves_trip_day_detail_view(client, trip_day: TripDay) -> None:
    trip_day_pk = str(trip_day.pk)
    view = resolve('/trips/days/' + trip_day_pk + '/')

    assert view.func.__name__ == TripDayDetailView.as_view().__name__


# TripDay Update View tests


def test_trip_day_update(client, trip_day: TripDay) -> None:
    trip_day_pk = {'pk': trip_day.pk}
    context = {
        'notes': 'These are updated notes.',
    }
    response = client.post(reverse('trips:trip_day_update', kwargs=trip_day_pk), data=context)
    trip_day.refresh_from_db()

    assert response.status_code == 302
    assert trip_day.notes == 'These are updated notes.'


# ==============================================================================
# ACTIVITY TESTS
# ==============================================================================

# Activity Create View tests


def test_activity_create(client, trip_day: TripDay) -> None:
    trip_day_pk = {'pk': trip_day.pk}
    context = {
        'title': 'New test activity',
        'time': datetime.time(hour=11, minute=11),
    }
    response = client.post(reverse('trips:activity_create', kwargs=trip_day_pk), data=context)
    new_activity = Activity.objects.get(title='New test activity')

    assert response.status_code == 302
    assert new_activity.day == trip_day


# TripDay Update View tests


def test_activity_update(client, activity: Activity) -> None:  
    activity_pk = {'pk': activity.pk}
    context = {
        'title': 'These are updated notes.',
        "time": activity.time,
    }
    response = client.post(reverse('trips:activity_update', kwargs=activity_pk), data=context)
    activity.refresh_from_db()

    assert response.status_code == 302
    assert activity.title == 'These are updated notes.'
