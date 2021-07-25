import pytest
from django.urls import reverse


# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(username='john', password='testpass123')
    return user


# ==============================================================================
# HOME PAGE TESTS
# ==============================================================================


def test_homepage_logged_in_status_code_200(client, user):
    client.force_login(user)
    response = client.get('/')

    assert response.status_code == 200


def test_homepage_logged_in_url_name(client, user):
    client.force_login(user)
    response = client.get(reverse("pages:home"))

    assert response.status_code == 200


def test_homepage_logged_in_template(client, user):
    client.force_login(user)
    response = client.get('/')
    homepage_template_name = ['pages/home.html']

    assert response.template_name == homepage_template_name


def test_homepage_not_logged_in_status_code_302(client):
    response = client.get('/')

    assert response.status_code == 302


@pytest.mark.django_db
def test_homepage_not_logged_in_redirect_to_login(client):
    response = client.get('/')
    # redirected_login_url:
    redirected_login_url = "/accounts/login/?next=/"  # equivalent to django settings.LOGIN_URL + "?next=/"

    assert response.url == redirected_login_url
