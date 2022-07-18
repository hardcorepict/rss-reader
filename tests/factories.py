import factory
import pytz

from channel.models import Channel, Subscription
from mail.services import Mail
from post.models import Action, Post
from user.models import User


class MailFactory(factory.Factory):
    class Meta:
        model = Mail


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    password = factory.Faker("password")
    is_active = True

    class Meta:
        model = User


class ChannelFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Channel {n}")
    url = factory.Sequence(lambda n: f"http://channel_{n}")

    class Meta:
        model = Channel


class SubscriptionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("tests.factories.UserFactory")
    channel = factory.SubFactory("tests.factories.ChannelFactory")

    class Meta:
        model = Subscription


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Post_{n}")
    channel = factory.SubFactory("tests.factories.ChannelFactory")
    url = factory.LazyAttribute(lambda obj: f"{obj.channel.url}/{obj.title}")
    description = factory.Faker("text")
    published_date = factory.Faker("date_time", tzinfo=pytz.UTC)

    class Meta:
        model = Post


class ActionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("tests.factories.UserFactory")
    post = factory.SubFactory("tests.factories.PostFactory")

    class Meta:
        model = Action
