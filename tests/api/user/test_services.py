import factories as f
import pytest

from user.models import User
from user.services import UserService


class TestUserService:
    def test_create_user(self):
        user_data = {"email": "test@example.com", "password": "test"}
        srv = UserService()
        srv.create_user(**user_data)

        users = User.objects.all()

        assert users.count() == 1
        assert users[0].email == user_data["email"]

    def test_create_user__when_no_email(self):
        user_data = {"email": "", "password": "test"}
        srv = UserService()

        with pytest.raises(ValueError):
            srv.create_user(**user_data)

        users = User.objects.all()
        assert len(users) == 0

    def test_set_password(self):
        user = f.UserFactory()
        new_password = "qwertyuiop"

        srv = UserService()
        srv.set_password(user, new_password)

        assert user.check_password(new_password) is True

    def test_set_password__when_empty_password(self):
        user = f.UserFactory()
        new_password = ""

        srv = UserService()
        with pytest.raises(ValueError):
            srv.set_password(user, new_password)

        assert user.check_password(new_password) is False
