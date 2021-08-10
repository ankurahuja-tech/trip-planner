import pytest
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

pytestmark = pytest.mark.django_db


def test_create_user() -> None:
    user = CustomUser.objects.create_user(username="john", email="john@email.com", password="testpass123")

    assert CustomUser.objects.all().count() == 1
    assert user.username == "john"
    assert user.email == "john@email.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


def test_create_superuser() -> None:
    admin_user = CustomUser.objects.create_superuser(
        username="superadmin", email="superadmin@email.com", password="testpass123"
    )

    assert admin_user.username == "superadmin"
    assert admin_user.email == "superadmin@email.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
