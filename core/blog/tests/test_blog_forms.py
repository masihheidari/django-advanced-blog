from django.test import SimpleTestCase
from ..forms import PostForm
from datetime import datetime


class TestPostForm(SimpleTestCase):

    def test_post_form_with_valid_data(self):
        form = PostForm(
            data={
                "title": "test",
                "content": "bio",
                "status": True,
                "published_date": datetime.now(),
            }
        )
        self.assertTrue(form.is_valid())
