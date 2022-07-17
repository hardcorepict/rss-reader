from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import (
    ResetPasswordConfirmSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)
from .services import UserService


class UserViewSet(GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    user_service = UserService()

    def create(self, request: HttpRequest) -> HttpResponse:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.user_service.create_user(**serializer.validated_data)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def current(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def reset_password(self, request: HttpRequest) -> HttpResponse:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data["email"])
        self.user_service.reset_password(user, request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def reset_password_confirm(self, request: HttpRequest) -> HttpResponse:
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        self.user_service.set_password(
            user=user, password=serializer.validated_data["password"]
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
