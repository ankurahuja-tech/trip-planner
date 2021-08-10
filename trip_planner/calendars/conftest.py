import pytest

from config.settings.base import AUTH_USER_MODEL

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
