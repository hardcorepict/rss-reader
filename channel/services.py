from app.base.services import BaseService
from user.models import User

from .exceptions import AlreadySusbcribed, NotSubscribed
from .models import Channel, Subscription


class ChannelService:
    def __init__(self) -> None:
        self.model = Channel

    def create_channel(self, title: str, url: str) -> Channel:
        channel, _ = self.model.objects.get_or_create(title=title, url=url)
        return channel


class SubscriptionService(BaseService):
    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.model = Subscription

    def subscribe(self, channel) -> None:
        subscription, created = self.model.objects.get_or_create(
            user=self.user, channel=channel
        )
        if not created:
            raise AlreadySusbcribed

    def unsubscribe(self, channel: Channel) -> None:
        try:
            subscription = Subscription.objects.get(user=self.user, channel=channel)
        except Subscription.DoesNotExist:
            raise NotSubscribed
        subscription.delete()
