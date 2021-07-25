import pytest
from django.urls import reverse, resolve

from trip_planner.pages.views import HomePageView


# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def user(client, django_user_model):
    user = django_user_model.objects.create_user(username='john', password='testpass123')
    client.force_login(user)
    return user


# ==============================================================================
# HOME PAGE TESTS
# ==============================================================================


# Tests for when user is logged in


def test_homepage_logged_in_url_status_code_200(client, user):
    response = client.get('/')
    assert response.status_code == 200


def test_homepage_logged_in_url_dispatcher_status_code_200(client, user):
    response = client.get(reverse("pages:home"))
    assert response.status_code == 200


def test_homepage_logged_in_template(client, user):
    response = client.get(reverse("pages:home"))
    homepage_template_name = ['pages/home.html']
    assert response.template_name == homepage_template_name


def test_homepage_url_resolves_homepageview(client, user):
    view = resolve('/')
    assert view.func.__name__ == HomePageView.as_view().__name__


# Tests for when user is notlogged in


def test_homepage_not_logged_in_status_code_302(client):
    response = client.get(reverse("pages:home"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_homepage_not_logged_in_redirect_to_login(client):
    response = client.get(reverse("pages:home"))
    redirected_login_url = "/accounts/login/?next=/"  # equivalent to django settings.LOGIN_URL + "?next=/"
    assert response.url == redirected_login_url
