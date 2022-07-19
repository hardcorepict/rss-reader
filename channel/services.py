import urllib.parse

from app.base.services import BaseParser, BaseService
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


class RssChannelParser(BaseParser):
    def __init__(self, url):
        super().__init__(url)
        self.links = []

    def get_rss(self):
        self.parse()
        links = self.soup.find_all("link", attrs={"type": "application/rss+xml"})
        return [self._make_rss(link) for link in links]

    def _make_rss(self, data):
        return Channel(
            title=data["title"], url=urllib.parse.urljoin(self.url, data["href"])
        )
