from django.db.models import Q
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from ...models import Post, Category
from .serializers import (
    PostSerializer,
    PostListSerializer,
    CategorySerializer,
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .paginations import StandardResultsSetPagination


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_date", "published_date"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Used by drf-yasg to build the schema, no real request involved.
        if getattr(self, "swagger_fake_view", False):
            return Post.objects.none()

        queryset = Post.objects.select_related("author__user", "category")
        user = self.request.user
        if user.is_authenticated:
            # Published posts for everyone, plus the user's own drafts.
            return queryset.filter(
                Q(is_published=True) | Q(author__user=user)
            )
        return queryset.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()