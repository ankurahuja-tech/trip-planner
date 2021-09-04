import pytest
from django.conf import settings
from django.core import mail
from django.urls import resolve, reverse

from config.settings.base import AUTH_USER_MODEL
from trip_planner.pages.views import ContactPageView, HomePageView

# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def user(client, django_user_model: AUTH_USER_MODEL) -> AUTH_USER_MODEL:
    user = django_user_model.objects.create_user(username="john", password="testpass123")
    client.force_login(user)
    return user


# ==============================================================================
# HOME PAGE TESTS
# ==============================================================================


# Tests for when user is logged in


def test_homepage_logged_in_url_status_code_200(client, user):
    response = client.get("/")
    assert response.status_code == 200


def test_homepage_logged_in_url_dispatcher_status_code_200(client, user):
    response = client.get(reverse("pages:home"))
    assert response.status_code == 200


def test_homepage_logged_in_template(client, user):
    response = client.get(reverse("pages:home"))
    homepage_template_name = "pages/home.html"
    assert homepage_template_name in response.template_name


def test_homepage_url_resolves_homepageview(client, user):
    view = resolve("/")
    assert view.func.__name__ == HomePageView.as_view().__name__


# Tests for when user is notlogged in


def test_homepage_not_logged_in_status_code_200(client):
    response = client.get(reverse("pages:home"))
    assert response.status_code == 200


# ==============================================================================
# CONTACT PAGE TESTS
# ==============================================================================


def test_contactpage_logged_in_url_status_code_200(client, user):
    response = client.get("/")
    assert response.status_code == 200


def test_contactpage_logged_in_url_dispatcher_status_code_200(client, user):
    response = client.get(reverse("pages:contact"))
    assert response.status_code == 200


def test_contactpage_logged_in_template(client, user):
    response = client.get(reverse("pages:contact"))
    contactpage_template_name = "pages/contact.html"
    assert contactpage_template_name in response.template_name


def test_contactpage_url_resolves_contactpageview(client, user):
    view = resolve("/contact/")
    assert view.func.__name__ == ContactPageView.as_view().__name__


# Tests for when user is notlogged in


def test_contactpage_not_logged_in_status_code_200(client):
    response = client.get(reverse("pages:contact"))
    assert response.status_code == 200


def test_send_contact_email(client):
    cleaned_name = "testuser"
    cleaned_email = "testuser@email.com"
    cleaned_subject = "This is a test subject."
    cleaned_message = "This is a test message."

    expected_subject = f"Trip Planner: {cleaned_name} / {cleaned_email} said:"
    expected_message = f"{cleaned_name} / {cleaned_email} said:"
    expected_message += f"\n\nsubject: {cleaned_subject}"
    expected_message += f"\n\nmessage: {cleaned_message}"

    mail.send_mail(
        subject=expected_subject,
        message=expected_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            settings.DEFAULT_FROM_EMAIL,
        ],
    )

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Trip Planner: testuser / testuser@email.com said:"
    assert (
        mail.outbox[0].body
        == "testuser / testuser@email.com said:\n\nsubject: This is a test subject.\n\nmessage: This is a test message."
    )
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].to == [settings.DEFAULT_FROM_EMAIL]
