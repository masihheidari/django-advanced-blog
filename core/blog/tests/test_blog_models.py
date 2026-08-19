from django.test import TestCase
from ..models import Post, Category
from datetime import datetime
from accounts.models import User, Profile


class TestPostModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='testtesttest@gmail.com', password='1qaa@qa3')
        self.category = Category.objects.create(name='Test Category')

        # signal خودش یک Profile خالی ساخته؛ فقط مقادیرش رو پر می‌کنیم
        self.profile = self.user.profile_set.first()
        self.profile.first_name = 'test_first_name'
        self.profile.last_name = 'test_last_name'
        self.profile.bio = 'test_bio'
        self.profile.save()  

    def test_create_post_with_valid_data(self):
 

        post = Post.objects.create(
            title='testtest',
            author=self.profile,
            content="bio",
            status=True,
            category=self.category,
            published_date=datetime.now()
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())