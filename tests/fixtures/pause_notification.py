import pytest


@pytest.fixture(scope="function")
def pause_notification(mock_account_notification_create, mock_account_notification_update,
                       mock_address_notification_update):
    return True
