from typing import Iterable

from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Post


class PostFilter(filters.FilterSet):

    unread_only = filters.BooleanFilter(method="get_unread_posts")
    bookmarked = filters.BooleanFilter(method="get_bookmarked_posts")
    search = filters.CharFilter(method="search_text")

    class Meta:
        model = Post
        fields = ["unread_only", "bookmarked", "channel", "search"]

    def get_unread_posts(
        self, queryset: Iterable[Post], name: str, value: str
    ) -> Iterable[Post]:
        if value:
            queryset = queryset.unread(user=self.request.user)
        return queryset

    def get_bookmarked_posts(
        self, queryset: Iterable[Post], name: str, value: str
    ) -> Iterable[Post]:
        if value:
            queryset = queryset.bookmarked(user=self.request.user)
        return queryset

    def search_text(
        self, queryset: Iterable[Post], name: str, value: str
    ) -> Iterable[Post]:
        if value:
            queryset = queryset.filter(
                Q(title__icontains=value) | Q(description__icontains=value)
            )
        return queryset
