from django.urls import reverse

from tests import factories as f
from tests.conftest import api_client, test_user, test_user_api_client
from tests.utils import get_response_content


class TestUserView:
    def test_user_create(self, api_client):
        data = {"email": "test_user@test.com", "password": "123"}
        url = reverse("users-list")
        response = api_client.post(url, data=data)

        assert response.status_code == 201

        response_data = get_response_content(response)
        assert response_data["email"] == data["email"]

    def test_user_create__when_user_with_that_name_exists(self, api_client):
        user = f.UserFactory.create(email="test_user@test.com")
        url = reverse("users-list")
        data = {"email": "test_user@test.com", "password": "123"}
        response = api_client.post(url, data=data)

        assert response.status_code == 400

    def test_user_current(self, test_user, test_user_api_client):
        url = reverse("users-current")
        response = test_user_api_client.get(url)

        assert response.status_code == 200

        data = get_response_content(response)
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email

    def test_user_current__when_not_authorized(self, api_client):
        url = reverse("users-current")
        response = api_client.get(url)

        assert response.status_code == 401
