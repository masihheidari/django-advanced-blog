import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import User
from blog.models import Category, Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_user(db):
    return User.objects.create_user(
        email="swdd@kdcdkffk.com", password="1qa@/fkkdle"
    )


@pytest.fixture
def common_profile(common_user):
    profile = common_user.profile
    profile.first_name = "test"
    profile.last_name = "test"
    profile.bio = "test bio"
    profile.save()
    return profile


@pytest.fixture
def common_category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@example.com", password="1qa@/fkkdle"
    )


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
            "is_published": True,
            "published_date": timezone.now().isoformat(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_status(
        self, api_client, common_user, common_profile, common_category
    ):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "is_published": True,
            "category": common_category.name,
            "published_date": timezone.now().isoformat(),
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert response.data["author"] == common_profile.id

    def test_created_published_post_is_visible_to_anonymous(
        self, api_client, common_user, common_profile, common_category
    ):
        api_client.force_authenticate(user=common_user)
        response = api_client.post(
            reverse("blog:api-v1:post-list"),
            {
                "title": "visible",
                "content": "description",
                "is_published": True,
                "category": common_category.name,
            },
        )
        api_client.force_authenticate(user=None)
        detail_url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": response.data["id"]}
        )
        assert api_client.get(detail_url).status_code == 200

    def test_draft_is_visible_only_to_its_author(
        self, api_client, common_user, common_profile, common_category
    ):
        post = Post.objects.create(
            title="draft",
            content="secret",
            author=common_profile,
            category=common_category,
            is_published=False,
        )
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.pk})

        assert api_client.get(url).status_code == 404

        api_client.force_authenticate(user=common_user)
        assert api_client.get(url).status_code == 200

    def test_create_post_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("blog:api-v1:post-list")
        data = {"title": "test", "content": "description"}
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestCategoryApi:

    def test_regular_user_cannot_create_category(
        self, api_client, common_user
    ):
        api_client.force_authenticate(user=common_user)
        response = api_client.post(
            reverse("blog:api-v1:category-list"), {"name": "New"}
        )
        assert response.status_code == 403

    def test_admin_can_create_category(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(
            reverse("blog:api-v1:category-list"), {"name": "New"}
        )
        assert response.status_code == 201

    def test_anyone_can_list_categories(self, api_client):
        response = api_client.get(reverse("blog:api-v1:category-list"))
        assert response.status_code == 200