from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from .filters import PostFilter
from .models import Post
from .paginators import PostPagination
from .serializers import PostSerializer
from .services import PostActionService


class PostViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(channel__subscriptions__user=user)
        return queryset

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        post = self.get_object()
        service = PostActionService.build_from_request(request)
        service.mark_as_read(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def mark_as_unread(self, request, pk=None):
        post = self.get_object()
        service = PostActionService.build_from_request(request)
        service.mark_as_unread(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def add_to_bookmarks(self, request, pk=None):
        post = self.get_object()
        service = PostActionService.build_from_request(request)
        service.add_to_bookmarks(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def remove_from_bookmarks(self, request, pk=None):
        post = self.get_object()
        service = PostActionService.build_from_request(request)
        service.remove_from_bookmarks(post)
        return Response(status=status.HTTP_204_NO_CONTENT)
