import pytest

from src import services


@pytest.fixture(scope="function")
def seed_account():
    pytest.account = services.AccountService().create(status='pending', role='member', user_uuid=pytest.user_uuid,
                                                      email=pytest.email, display_name=pytest.display_name,
                                                      username=pytest.username)
