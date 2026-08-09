from rest_framework import serializers

from ...models import Post

# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     id = serializers.IntegerField()


class PostSerializer(serializers.ModelSerializer):


    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'category', 'created_date', 'published_date', 'id']
