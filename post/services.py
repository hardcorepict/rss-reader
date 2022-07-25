from app.base.services import BaseParser, BaseService, DatetimeService
from channel.models import Channel

from .exceptions import AlreadyBookmarked, AlreadyRead, NotBookmarkedYet, NotReadYet
from .models import Action, Post


class PostActionService(BaseService):
    def __init__(self, user):
        super().__init__(user)
        self.model = Action

    def mark_as_read(self, post: Post) -> None:
        action, created = Action.objects.get_or_create(user=self.user, post=post)
        if action.is_read:
            raise AlreadyRead
        action.is_read = True
        action.save()

    def mark_as_unread(self, post: Post) -> None:
        try:
            action = Action.objects.get(user=self.user, post=post)
        except Action.DoesNotExist:
            raise NotReadYet

        if not action.is_read:
            raise NotReadYet

        action.is_read = False
        action.save()

    def add_to_bookmarks(self, post: Post) -> None:
        action, created = Action.objects.get_or_create(user=self.user, post=post)
        if action.bookmarked:
            raise AlreadyBookmarked
        action.bookmarked = True
        action.save()

    def remove_from_bookmarks(self, post: Post) -> None:
        try:
            action = Action.objects.get(user=self.user, post=post)
        except Action.DoesNotExist:
            raise NotBookmarkedYet

        if not action.bookmarked:
            raise NotBookmarkedYet

        action.bookmarked = False
        action.save()


class PostParser(BaseParser):
    def __init__(self, channel: Channel):
        super().__init__(url=channel.url, parser="xml")
        self.channel = channel

    def get_posts(self):
        self.parse()
        raw_posts = self.soup.find_all("item")
        posts = [self.make_post(post) for post in raw_posts]
        return posts

    def make_post(self, post_data) -> Post:
        kwargs = {
            "title": post_data.title.text,
            "url": post_data.link.text,
            "description": post_data.description.text,
            "channel": self.channel,
        }
        date_srv = DatetimeService()
        try:
            published_date = date_srv.to_utc(date_srv.from_str(post_data.pubDate.text))
        except ValueError:
            return

        author = post_data.creator.text if post_data.creator else self.channel.title
        kwargs.update({"author": author, "published_date": published_date})
        return Post(**kwargs)


class PostService:
    def __init__(self):
        self.model = Post

    def bulk_create(self, posts: list[Post]) -> None:
        self.model.objects.bulk_create(posts, ignore_conflicts=True)
