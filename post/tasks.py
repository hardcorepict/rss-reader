from django.conf import settings
from django.shortcuts import get_object_or_404

from app import celery_app
from channel.models import Channel
from post.services import PostParser, PostService


@celery_app.task
def fetch_all_posts():
    channels = Channel.objects.all()
    for channel in channels:
        fetch_posts_by_channel.delay(channel.id)


@celery_app.task()
def fetch_posts_by_channel(channel_id):
    channel = get_object_or_404(Channel, pk=channel_id)
    parser = PostParser(channel)
    posts = parser.get_posts()
    PostService().bulk_create(posts)


celery_app.conf.beat_schedule = {
    "fetch_all_posts": {
        "task": "post.tasks.fetch_all_posts",
        "schedule": settings.DEFAULT_REFRESH_TIME,
    },
}
celery_app.conf.timezone = "UTC"
