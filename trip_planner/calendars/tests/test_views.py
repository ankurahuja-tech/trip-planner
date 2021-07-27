import pytest
from django.urls import reverse, resolve


# ==============================================================================
# FIXTURES
# ==============================================================================

pytestmark = pytest.mark.django_db

# ==============================================================================
# SIGN UP PAGE TESTS
# ==============================================================================


def test_calendar_url_status_code_200(client):
    response = client.get('/calendar/')
    assert response.status_code == 200


def test_calendar_url_dispatcher_status_code_200(client):
    response = client.get(reverse('calendars:calendar'))
    assert response.status_code == 200
