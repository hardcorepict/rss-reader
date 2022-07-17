import factories as f
import pytest
from utils import APIClient


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
