import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    """
    Supports:
    - ?category=<id>        → filter by category
    - ?author=<id>          → filter by author
    - ?status=draft|published → filter by status
    """

    category = django_filters.NumberFilter(
        field_name="categories__id",
        label="Category ID",
    )

    class Meta:
        model = Post
        fields = ["status", "author", "category"]
