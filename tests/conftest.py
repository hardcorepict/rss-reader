import factories as f
import pytest
from utils import APIClient, get_tokens_for_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True, scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    django_db_blocker.unblock()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "redis://",
        "result_backend": "redis://",
    }


@pytest.fixture
def test_user():
    return f.UserFactory.create()


@pytest.fixture
def test_user_api_client(api_client, test_user):
    tokens = get_tokens_for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    api_client.login(test_user)
    return api_client
