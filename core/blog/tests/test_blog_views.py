from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Profile
from blog.models import Post, Category
from django.utils import timezone


class TestBlogView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testtesttest@gmail.com', password='1qaa@qa3')
        self.category = Category.objects.create(name='Test Category')

        self.profile = self.user.profile_set.first()
        self.profile.first_name = 'test_first_name'
        self.profile.last_name = 'test_last_name'
        self.profile.bio = 'test_bio'
        self.profile.save()

        self.post = Post.objects.create(
            title='testtest',
            author=self.profile,
            content="bio",
            status=True,
            category=self.category,
            published_date=timezone.now()
        )

    def test_blog_index_url_successful_response(self):
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')

    def test_blog_post_detail_logged_in_response(self):
        self.client.force_login(self.user)
        url = reverse('blog:post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_post_detail_anonymous_response(self):
        url = reverse('blog:post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)