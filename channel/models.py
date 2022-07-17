from django.conf import settings
from django.db import models


class ChannelQuerySet(models.QuerySet):
    def is_subscribed(self, user):
        return self.filter(subscriptions__user=user)


class Channel(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Subscription")

    objects = ChannelQuerySet.as_manager()

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="subscriptions"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "channel"),)
