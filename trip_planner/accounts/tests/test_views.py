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
# def test_signup_form(client, django_user_model):
#     credentials = {
#         "username": "janek",
#         "email": "janek@email.com",
#         "password": "TesterowyPass#469",
#         "password2": "TesterowyPass"
#         }
#     response = client.post(reverse('account_signup'), data=credentials, follow=True)
#     assert response.status_code == 200

#     users = django_user_model.objects.all()
#     assert users.count() == 1


# ==============================================================================
# LOGIN PAGE TESTS
# ==============================================================================


def test_login_url_status_code_200(client):
    response = client.get('/accounts/login/')
    assert response.status_code == 200


def test_login_url_dispatcher_status_code_200(client):
    response = client.get(reverse('account_login'))
    assert response.status_code == 200


# TODO: how to test that login form works?
# def test_login(client, django_user_model):
#     credentials = {
#         "username": "jack",
#         "password": "testpass123",
#         "is_active": True,
#         "is_staff": True,
#         "is_superuser": True,
#     }
#     user = django_user_model.objects.create_user(**credentials)
#     user.save()
#     response = client.get('/accounts/login/', credentials, follow=True)
#     assert response.context["user"].is_authenticated == True
