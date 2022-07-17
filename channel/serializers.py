from rest_framework import serializers

from .models import Channel


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ["id", "title", "url"]


class FeedSerializer(serializers.Serializer):
    title = serializers.CharField()
    url = serializers.URLField()
