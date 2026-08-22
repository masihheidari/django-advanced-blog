from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from blog.models import Category
from datetime import datetime
import pytest


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="swdd@kdcdkffk.com",
        password="1qa@/fkkdle"
        )
    return user


@pytest.fixture
def common_profile(common_user):
    profile = common_user.profile_set.first()
    profile.first_name = "test"
    profile.last_name = "test"
    profile.bio = "test bio"
    profile.save()
    return profile


@pytest.fixture
def common_category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestPostApi:

    def test_get_post_response_200_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "pytest",
            "content": "wer",
            "status": True,
            "published_date": datetime.now(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_status(
        self, api_client, common_user, common_profile, common_category
    ):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "author": common_profile.id,
            "content": "description",
            "status": True,
            "category": common_category.name,
            "published_date": datetime.now(),
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_post_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("blog:api-v1:post-list")
        data = {"title": "test", "content": "description"}
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 400
