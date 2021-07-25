import pytest
from django.urls import reverse, resolve


# ==============================================================================
# FIXTURES
# ==============================================================================

pytestmark = pytest.mark.django_db

# ==============================================================================
# SIGN UP PAGE TESTS
# ==============================================================================


def test_signup_url_status_code_200(client):
    response = client.get('/accounts/signup/')
    assert response.status_code == 200


def test_signup_url_dispatcher_status_code_200(client):
    response = client.get(reverse('account_signup'))
    assert response.status_code == 200


# TODO: how to test that correct form creates a user?
# def test_signup_form(client):
#     response = client.post('/accounts/signup/', {"username": "Janek", "password": "testpass123", "password2": "testpass123"})
#     assert response.status_code == 201


# ==============================================================================
# LOGIN PAGE TESTS
# ==============================================================================


def test_signup_url_status_code_200(client):
    response = client.get('/accounts/login/')
    assert response.status_code == 200


def test_signup_url_dispatcher_status_code_200(client):
    response = client.get(reverse('account_login'))
    assert response.status_code == 200
