from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from post.tasks import fetch_posts_by_channel

from .models import Channel
from .serializers import (
    ChannelSerializer,
    FeedSerializer,
    RssChannelSerializer,
    UrlChannelSerializer,
)
from .services import ChannelService, RssChannelParser, SubscriptionService


class ChannelViewSet(GenericViewSet):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Channel]:
        user = self.request.user
        return Channel.objects.is_subscribed(user)

    def create(self, request: HttpRequest) -> HttpResponse:
        serializer = FeedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = ChannelService()
        channel = service.create_channel(**serializer.validated_data)
        serializer = ChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: HttpRequest) -> HttpResponse:
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def subscribe(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        channel = get_object_or_404(Channel, id=pk)
        srv = SubscriptionService.build_from_request(request)
        srv.subscribe(channel)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        channel = self.get_object()
        srv = SubscriptionService.build_from_request(request)
        srv.unsubscribe(channel)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def get_rss(self, request):
        serializer = UrlChannelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = RssChannelParser(**serializer.validated_data)
        rss = service.get_rss()
        response_serializer = RssChannelSerializer(rss, many=True)
        return Response(response_serializer.data)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def refresh(self, request, pk: int = None):
        channel = self.get_object()
        fetch_posts_by_channel(channel)
        return Response(status=status.HTTP_204_NO_CONTENT)
