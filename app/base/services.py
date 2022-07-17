from typing import TypeVar

from django.http import HttpRequest

from user.models import User

T = TypeVar("T")


class BaseService:
    def __init__(self, user: User):
        self.user = user
        self.model = None

    @classmethod
    def build_from_request(cls: T, request: HttpRequest) -> T:
        user = request.user if request.user and not request.user.is_anonymous else None
        return cls(user)
