import pytest
from django.urls import resolve, reverse

from config.settings.base import AUTH_USER_MODEL
from trip_planner.calendars.views import CalendarView

# ==============================================================================
# CALENDAR TESTS
# ==============================================================================


def test_calendar_url_dispatcher(client, user: AUTH_USER_MODEL) -> None:
    response = client.get(reverse("calendars:calendar"))
    calendar_view_template_name = "calendars/calendar.html"

    assert response.status_code == 200
    assert calendar_view_template_name in response.template_name


def test_calendar_url(client, user: AUTH_USER_MODEL) -> None:
    response = client.get("/calendar/")

    assert response.status_code == 200


def test_calendar_url_resolves_calendarview(client) -> None:
    view = resolve("/calendar/")

    assert view.func.__name__ == CalendarView.as_view().__name__
