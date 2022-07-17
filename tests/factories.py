import factory

from mail.services import Mail
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
