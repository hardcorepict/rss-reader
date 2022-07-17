import factories as f
import pytest

from channel.exceptions import AlreadySusbcribed, NotSubscribed
from channel.models import Channel
from channel.services import ChannelService, SubscriptionService


class TestSubscriptionService:
    def test_subscribe_channel(self):
        user = f.UserFactory()
        channel = f.ChannelFactory()

        srv = SubscriptionService(user)
        srv.subscribe(channel)

        assert user.subscriptions.count() == 1

    def test_subscribe_channel__when_already_subscribed(self):
        user = f.UserFactory()
        channel = f.ChannelFactory()
        f.SubscriptionFactory(user=user, channel=channel)

        srv = SubscriptionService(user)
        with pytest.raises(AlreadySusbcribed):
            srv.subscribe(channel)

    def test_unsubscribe_channel(self):
        user = f.UserFactory()
        channel_1 = f.ChannelFactory()
        channel_2 = f.ChannelFactory()

        subscription_1 = f.SubscriptionFactory(user=user, channel=channel_1)
        subscription_2 = f.SubscriptionFactory(user=user, channel=channel_2)

        srv = SubscriptionService(user)
        srv.unsubscribe(channel_1)
        subscriptions = user.subscriptions.all()

        assert subscriptions.count() == 1
        assert subscriptions[0] == subscription_2

    def test_unsubscribe_channel__when_not_subscribed(self):
        user = f.UserFactory()
        channel_1 = f.ChannelFactory()
        channel_2 = f.ChannelFactory()

        subscription = f.SubscriptionFactory(user=user, channel=channel_2)

        srv = SubscriptionService(user)
        with pytest.raises(NotSubscribed):
            srv.unsubscribe(channel_1)

        subscriptions = user.subscriptions.all()

        assert subscriptions.count() == 1
        assert subscriptions[0] == subscription


class TestChannelService:
    def test_create_channel(self):
        data = {"title": "test", "url": "http://test.com/rss"}
        srv = ChannelService()
        channel = srv.create_channel(**data)

        channels = Channel.objects.all()
        assert channels.count() == 1
