from rest_framework import serializers

from categories.serializers import CategorySerializer
from users.serializers import UserSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    categories_detail = CategorySerializer(source="categories", many=True, read_only=True)

    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=__import__("categories.models", fromlist=["Category"]).Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source="categories",
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "author",
            "status",
            "categories_detail",
            "category_ids",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author", "created_at", "updated_at")
