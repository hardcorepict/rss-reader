from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User
from .utils import decode_uid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class ResetPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        uid = decode_uid(data["uid"])
        try:
            user = get_object_or_404(User, pk=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid uid")

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid token")

        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")

        data["user"] = user
        return data
