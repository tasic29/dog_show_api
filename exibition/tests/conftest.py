from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest

from core.models import MyUser


@pytest.fixture
def api_client():
    return APIClient()


# @pytest.fixture
# def authenticate(api_client):
#     def do_authenticate(is_staff=False):
#         return api_client.force_authenticate(user=MyUser(is_staff=is_staff))
#     return do_authenticate


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        user = MyUser.objects.create(username='testuser', is_staff=is_staff)
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate
