from django.conf import settings
from user.models import User


class Template:
    WELCOME = "welcome"
    RESET_PASSWORD = "reset_password"
    RESET_PASSWORD_SUCCESS = "reset_password_success"


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


class MailService:
    @staticmethod
    def send_welcome_email(user: User):
        mail = Mail(
            template=Template.WELCOME,
            recipients=[user.email],
            context={"email": user.email},
        )
        mail.send()

    @staticmethod
    def send_success_email(user: User):
        mail = Mail(
            template=Template.RESET_PASSWORD_SUCCESS,
            recipients=[user.email],
            context={"email": user.email},
        )
        mail.send()

    @staticmethod
    def send_reset_password_email(user: User, link: str):
        mail = Mail(
            template=Template.RESET_PASSWORD,
            recipients=[user.email],
            context={
                "email": user.email,
                "link": link,
            },
        )
        mail.send()
