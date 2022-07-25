import factories as f
import pytest

from post.exceptions import AlreadyBookmarked, AlreadyRead, NotBookmarkedYet, NotReadYet
from post.models import Action, Post
from post.services import PostActionService


class TestPostActionService:

    service = PostActionService

    def test_mark_as_read(self):
        user = f.UserFactory()
        post = f.PostFactory()
        service = self.service(user)
        service.mark_as_read(post)

        action = Action.objects.get(user=user, post=post)

        assert action.is_read is True

    def test_mark_as_read__when_already_read(self):
        user = f.UserFactory()
        post = f.PostFactory()
        action = f.ActionFactory(user=user, post=post, is_read=True)
        service = self.service(user)

        with pytest.raises(AlreadyRead):
            service.mark_as_read(post)

    def test_mark_as_unread__when_not_read_and_no_action(self):
        user = f.UserFactory()
        post = f.PostFactory()
        service = self.service(user)

        with pytest.raises(NotReadYet):
            service.mark_as_unread(post)

    def test_mark_as_unread__when_not_read(self):
        user = f.UserFactory()
        post = f.PostFactory()
        action = f.ActionFactory(user=user, post=post)
        service = self.service(user)

        with pytest.raises(NotReadYet):
            service.mark_as_unread(post)

    def test_mark_as_unread__when_read(self):
        user = f.UserFactory()
        post = f.PostFactory()
        action = f.ActionFactory(user=user, post=post, is_read=True)
        service = self.service(user)
        service.mark_as_unread(post)
        action = Action.objects.get(user=user, post=post)

        assert action.is_read is False

    def test_add_to_bookmarks__when_no_action(self):
        user = f.UserFactory()
        post = f.PostFactory()
        service = self.service(user)
        service.add_to_bookmarks(post)

        action = Action.objects.get(user=user, post=post)
        assert action.bookmarked is True

    def test_add_to_bookmarks__when_action_exists(self):
        user = f.UserFactory()
        post = f.PostFactory()
        action = f.ActionFactory(user=user, post=post)
        service = self.service(user)
        service.add_to_bookmarks(post)

        action = Action.objects.get(user=user, post=post)
        assert action.bookmarked is True

    def test_add_to_bookmarks__when_bookmarked(self):
        user = f.UserFactory()
        post = f.PostFactory()
        action = f.ActionFactory(user=user, post=post, bookmarked=True)
        service = self.service(user)

        with pytest.raises(AlreadyBookmarked):
            service.add_to_bookmarks(post)

    def test_remove_from_bookmarks(self):
        user = f.UserFactory()
        post = f.PostFactory()
        action = f.ActionFactory(user=user, post=post, bookmarked=True)
        service = self.service(user)
        service.remove_from_bookmarks(post)

        action = Action.objects.get(user=user, post=post)
        assert action.bookmarked is False

    def test_remove_from_bookmarks__when_not_bookmarked(self):
        user = f.UserFactory()
        post = f.PostFactory()
        action = f.ActionFactory(user=user, post=post)
        service = self.service(user)
        with pytest.raises(NotBookmarkedYet):
            service.remove_from_bookmarks(post)

    def test_remove_from_bookmarks__when_not_bookmarked_no_action(self):
        user = f.UserFactory()
        post = f.PostFactory()
        service = self.service(user)
        with pytest.raises(NotBookmarkedYet):
            service.remove_from_bookmarks(post)
