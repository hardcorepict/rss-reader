from django.conf import settings
from django.db import models

from channel.models import Channel


class PostQuerySet(models.QuerySet):
    def bookmarked(self, user):
        return self.filter(actions__bookmarked=True)

    def unread(self, user):
        return self.exclude(actions__is_read=True)


class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    published_date = models.DateTimeField()
    url = models.URLField(unique=True)
    author = models.CharField(max_length=150)

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="posts")
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Action")

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.url


class Action(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actions"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="actions")

    is_read = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "post"),)
