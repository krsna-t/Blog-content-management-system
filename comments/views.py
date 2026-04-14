from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from posts.models import Post

from .models import Comment
from .permissions import IsCommentOwnerOrReadOnly
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related("user", "post")
        post_id = self.request.query_params.get("post")
        if post_id is not None:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        """comments allowed only on published posts."""
        post = serializer.validated_data["post"]
        if post.status != Post.Status.PUBLISHED:
            raise ValidationError(
                {"post": "Comments are only allowed on published posts."}
            )
        serializer.save(user=self.request.user)
