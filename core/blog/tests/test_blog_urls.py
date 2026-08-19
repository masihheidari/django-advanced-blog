from django.test import TestCase
from django.urls import reverse, resolve
from ..views import IndexView, PostDetailView


class TestUrl(TestCase):

    def test_blog_index_url_resolve(self):
        url = reverse("blog:index")
        self.assertEqual(resolve(url).func.view_class, IndexView)

    def test_blog_detail_url_resolve(self):
        url = reverse("blog:post-detail", kwargs={"pk": 4})
        self.assertEqual(resolve(url).func.view_class, PostDetailView)
