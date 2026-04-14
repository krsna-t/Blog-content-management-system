from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import PostFilter
from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Filtering & search
    filterset_class = PostFilter
    search_fields = ["title"]  # ?search=<term>
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Post.objects.select_related("author").prefetch_related("categories")

        if self.request.user.is_authenticated:
            from django.db.models import Q

            qs = qs.filter(Q(status=Post.Status.PUBLISHED) | Q(author=self.request.user))
        else:
            qs = qs.filter(status=Post.Status.PUBLISHED)

        return qs

    def perform_create(self, serializer):
        """Automatically assign the logged-in user as the post author."""
        serializer.save(author=self.request.user)
