from rest_framework import serializers

from ...models import Post, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    """Full representation, used for retrieve/create/update."""

    # Accepts the category name on input.
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "image",
            "content",
            "category",
            "is_published",
            "published_date",
            "created_date",
        ]
        read_only_fields = ["author"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Return the full category object instead of just its name.
        rep["category"] = (
            CategorySerializer(instance.category).data
            if instance.category
            else None
        )
        return rep


class PostListSerializer(PostSerializer):
    """Short representation, used for the list endpoint."""

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.ReadOnlyField(source="get_absolute_api_url")

    class Meta(PostSerializer.Meta):
        fields = [
            "id",
            "author",
            "title",
            "image",
            "snippet",
            "category",
            "relative_url",
            "is_published",
            "published_date",
            "created_date",
        ]