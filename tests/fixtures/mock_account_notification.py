import pytest

from tests.helpers import account_notification_create, account_notification_update


@pytest.fixture
def mock_account_notification_create(mocker):
    yield mocker.patch('src.decorators.account_notification.create', account_notification_create)


@pytest.fixture
def mock_account_notification_update(mocker):
    yield mocker.patch('src.decorators.account_notification.update', account_notification_update)
