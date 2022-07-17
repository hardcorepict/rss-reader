from django.contrib.auth.tokens import default_token_generator

from mail.services import MailService

from .models import User
from .utils import encode_uid, get_current_site


class UserService:
    def __init__(self):
        self.model = User

    def create_user(self, **user_data) -> User:
        user = self.model.objects.create_user(**user_data)
        MailService().send_welcome_email(user)
        return user

    def set_password(self, user: User, password: str) -> None:
        user.set_password(password)
        user.save()
        MailService().send_success_email(user)

    def reset_password(self, user: User, request) -> None:
        site = get_current_site(request)
        link = self.generate_recovery_link(user, site)
        MailService.send_reset_password_email(user, link)

    def generate_recovery_link(self, user: User, site: str) -> str:
        uid = encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        return f"{site}/reset/{uid}/{token}"
