from django.conf import settings


class Template:
    WELCOME = "welcome"
    RESET_PASSWORD = "reset_password"
    RESET_PASSWORD_CONFIRM = "reset_password_confirm"


class Mail:
    def __init__(
        self,
        template: Template,
        recipients: list[str],
        sender: str = settings.ADMIN_EMAIL,
        context: dict = {},
    ):
        self.template = template
        self.recipients = recipients
        self.sender = sender
        self.context = context

    def send(self):
        from .tasks import send_mail

        send_mail.delay(self)
