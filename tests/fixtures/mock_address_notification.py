import pytest

from tests.helpers import address_notification_update


@pytest.fixture
def mock_address_notification_update(mocker):
    yield mocker.patch('src.decorators.address_notification.update', address_notification_update)
