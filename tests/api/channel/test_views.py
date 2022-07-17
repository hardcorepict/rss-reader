import pytest
from django.urls import reverse

import tests.factories as f
from tests.conftest import api_client, test_user_api_client
from tests.utils import get_response_content, reverse_querystring


class TestChannelViewSet:
    def test_get_channels__when_has_no_subscriptions(self, test_user_api_client):
        channel_1 = f.ChannelFactory()

        url = reverse("channels-list")

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data == []

    def test_get_channels__when_not_authorized(self, api_client):
        channel_1 = f.ChannelFactory()

        url = reverse("channels-list")

        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_subscribed_channels(self, test_user, test_user_api_client):
        channel_1 = f.ChannelFactory()
        f.ChannelFactory()
        f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel_1)

        url = reverse_querystring("channels-list", query_kwargs={"is_subscribed": True})

        response = test_user_api_client.get(url)
        assert response.status_code == 200

        response_data = get_response_content(response)
        assert response_data[0]["id"] == channel_1.id
        assert response_data[0]["title"] == channel_1.title

    def test_subscribe_channel(self, test_user_api_client):
        channel = f.ChannelFactory()

        url = reverse("channels-subscribe", kwargs={"pk": channel.id})
        response = test_user_api_client.post(url)

        assert response.status_code == 201

    def test_subscribe_channel__when_already_subscribed(
        self, test_user, test_user_api_client
    ):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)

        url = reverse("channels-subscribe", kwargs={"pk": channel.id})
        response = test_user_api_client.post(url)

        assert response.status_code == 400

    def test_unsubscribe_channel__when_not_authorized(self, api_client):
        channel = f.ChannelFactory()

        url = reverse("channels-unsubscribe", kwargs={"pk": channel.id})
        response = api_client.post(url)

        assert response.status_code == 401

    def test_unsubscribe_channel(self, test_user, test_user_api_client):
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=test_user, channel=channel)

        url = reverse("channels-unsubscribe", kwargs={"pk": channel.id})
        response = test_user_api_client.post(url)

        assert response.status_code == 204

    def test_unsubscribe_channel__when_not_subscribed(self, test_user_api_client):
        channel = f.ChannelFactory()

        url = reverse("channels-unsubscribe", kwargs={"pk": channel.id})
        response = test_user_api_client.post(url)

        assert response.status_code == 404
