import factory

from mail.services import Mail


class MailFactory(factory.Factory):
    class Meta:
        model = Mail
