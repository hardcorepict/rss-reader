import factories as f
from django.urls import reverse

from post import exceptions as exc
from tests.conftest import api_client, test_user, test_user_api_client
from tests.utils import get_response_content, reverse_querystring


class TestPostViewSet:
    def test_get_posts(self, test_user, test_user_api_client):
        user = f.UserFactory()
        channels = [f.ChannelFactory() for _ in range(3)]
        posts = [f.PostFactory(channel=channels[i]) for i in range(3)]
        f.SubscriptionFactory(user=test_user, channel=channels[1])
        f.SubscriptionFactory(user=user, channel=channels[0])

        url = reverse("posts-list")

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 1
        assert len(response_data["results"]) == 1
        assert response_data["results"][0]["id"] == posts[1].id

    def test_get_posts__when_no_subscriptions(self, test_user_api_client):
        channel = f.ChannelFactory()
        [f.PostFactory(channel=channel) for _ in range(5)]

        url = reverse("posts-list")

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 0

    def test_get_posts__when_not_authorized(self, api_client):
        channel = f.ChannelFactory()
        [f.PostFactory(channel=channel) for _ in range(5)]

        url = reverse("posts-list")

        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_posts__when_filter_by_channel(self, test_user, test_user_api_client):
        channel_1 = f.ChannelFactory()
        channel_2 = f.ChannelFactory()
        channel_3 = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel_1)
        f.SubscriptionFactory(user=test_user, channel=channel_2)
        post = f.PostFactory(channel=channel_2)
        f.PostFactory(channel=channel_1)
        f.PostFactory(channel=channel_3)

        url = reverse_querystring("posts-list", query_kwargs={"channel": channel_2.id})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 1
        assert response_data["results"][0]["id"] == post.id

    def test_get_posts__when_filter_is_unread_only(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post_1 = f.PostFactory(channel=channel)
        post_2 = f.PostFactory(channel=channel)
        f.ActionFactory(user=test_user, post=post_1, is_read=True)

        url = reverse_querystring("posts-list", query_kwargs={"unread_only": True})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 1
        assert response_data["results"][0]["id"] == post_2.id

    def test_get_posts__when_filter_by_bookmarks(self, test_user, test_user_api_client):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(channel=channel)
        f.PostFactory(channel=channel)
        f.ActionFactory(user=test_user, post=post, bookmarked=True)

        url = reverse_querystring("posts-list", query_kwargs={"bookmarked": True})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 1
        assert response_data["results"][0]["id"] == post.id

    def test_get_posts__when_filter_by_search_in_title(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(title="test", channel=channel)
        f.PostFactory(title="text", channel=channel)
        f.ActionFactory(user=test_user, post=post, bookmarked=True)

        url = reverse_querystring("posts-list", query_kwargs={"search": "test"})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 1
        assert response_data["results"][0]["id"] == post.id

    def test_get_posts__when_filter_by_search_in_description(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(description="test", channel=channel)
        f.PostFactory(description="text", channel=channel)
        f.ActionFactory(user=test_user, post=post, bookmarked=True)

        url = reverse_querystring("posts-list", query_kwargs={"search": "test"})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 1
        assert response_data["results"][0]["id"] == post.id

    def test_get_posts__when_filter_by_search_no_match(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(title="test", channel=channel)
        f.PostFactory(description="test", channel=channel)
        f.ActionFactory(user=test_user, post=post, bookmarked=True)

        url = reverse_querystring("posts-list", query_kwargs={"search": "text"})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 0

    def test_get_posts__when_filter_by_search_no_value(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        f.PostFactory(channel=channel)
        f.PostFactory(channel=channel)

        url = reverse_querystring("posts-list", query_kwargs={"search": ""})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data["count"] == 2

    def test_mark_post_as_read__when_not_subscribed(self, test_user_api_client):
        post = f.PostFactory()

        url = reverse("posts-mark-as-read", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 404

    def test_mark_post_as_read(self, test_user, test_user_api_client):
        channel = f.ChannelFactory()
        post = f.PostFactory(channel=channel)
        f.SubscriptionFactory(user=test_user, channel=channel)

        url = reverse("posts-mark-as-read", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 204

    def test_mark_post_as_read__when_already_read(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        post = f.PostFactory(channel=channel)
        f.SubscriptionFactory(user=test_user, channel=channel)
        f.ActionFactory(user=test_user, post=post, is_read=True)

        url = reverse("posts-mark-as-read", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 400

        response_data = get_response_content(response)
        assert response_data["detail"] == exc.AlreadyRead.default_detail

    def test_mark_post_as_unread__when_unread(self, test_user, test_user_api_client):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(channel=channel)

        url = reverse("posts-mark-as-unread", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 400

        response_data = get_response_content(response)
        assert response_data["detail"] == exc.NotReadYet.default_detail

    def test_mark_post_as_unread(self, test_user, test_user_api_client):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(channel=channel)
        f.ActionFactory(user=test_user, post=post, is_read=True)

        url = reverse("posts-mark-as-unread", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 204

    def test_mark_post_as_unread__when_not_subscribed(self, test_user_api_client):
        post = f.PostFactory()

        url = reverse("posts-mark-as-unread", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 404

    def test_add_to_bookmarks(self, test_user, test_user_api_client):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(channel=channel)

        url = reverse("posts-add-to-bookmarks", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 204

    def test_add_to_bookmarks__when_not_subscribed(self, test_user_api_client):
        post = f.PostFactory()

        url = reverse("posts-add-to-bookmarks", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 404

    def test_add_to_bookmarks__when_already_bookmarked(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(channel=channel)
        f.ActionFactory(post=post, user=test_user, bookmarked=True)

        url = reverse("posts-add-to-bookmarks", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 400

        response_data = get_response_content(response)
        assert response_data["detail"] == exc.AlreadyBookmarked.default_detail

    def test_remove_from_bookmarks(self, test_user, test_user_api_client):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(channel=channel)
        f.ActionFactory(post=post, user=test_user, bookmarked=True)

        url = reverse("posts-remove-from-bookmarks", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 204

    def test_remove_from_bookmarks__when_not_bookmarked(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)
        post = f.PostFactory(channel=channel)
        f.ActionFactory(post=post, user=test_user)

        url = reverse("posts-remove-from-bookmarks", kwargs={"pk": post.id})

        response = test_user_api_client.post(url)
        assert response.status_code == 400

        response_data = get_response_content(response)
        assert response_data["detail"] == exc.NotBookmarkedYet.default_detail
