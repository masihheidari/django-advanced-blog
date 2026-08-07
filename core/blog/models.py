from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    # counted_view = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
