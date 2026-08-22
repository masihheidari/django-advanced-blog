from rest_framework import serializers

from ...models import Post, Category
from accounts.models import Profile


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(
        source="get_absolute_api_url",
        read_only=True
        )
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "author",
            "title",
            "image",
            "content",
            "snippet",
            "category",
            "relative_url",
            "created_date",
            "published_date",
            "id",
        ]
        read_only_fields = ["author"]

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        rep["state"] = "list"
        if request.resolver_match.kwargs.get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
        else:
            rep.pop("content", None)

        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}
        ).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]
