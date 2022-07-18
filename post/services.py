from app.base.services import BaseService

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
