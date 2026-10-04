from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from ..models import Post, Category


class TestPostModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testtesttest@gmail.com", password="1qaa@qa3"
        )
        self.category = Category.objects.create(name="Test Category")

        self.profile = self.user.profile
        self.profile.first_name = "test_first_name"
        self.profile.last_name = "test_last_name"
        self.profile.bio = "test_bio"
        self.profile.save()

    def test_create_post_with_valid_data(self):
        post = Post.objects.create(
            title="testtest",
            author=self.profile,
            content="bio",
            is_published=True,
            category=self.category,
            published_date=timezone.now(),
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())

    def test_snippet_returns_first_20_characters(self):
        post = Post.objects.create(
            title="t",
            author=self.profile,
            content="x" * 50,
            category=self.category,
        )
        self.assertEqual(post.get_snippet(), "x" * 20)

    def test_profile_is_created_automatically_for_new_user(self):
        self.assertEqual(self.user.profile.user, self.user)