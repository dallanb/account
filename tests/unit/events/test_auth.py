import time

import pytest

from src import events, services
from tests.helpers import generate_uuid


def test_auth_auth_created_sync(reset_db, pause_notification):
    """
    GIVEN 0 account instance and 0 address in the database
    WHEN directly calling event auth handle_event auth_created
    THEN it should add 1 account instance and 1 address instance to the database
    """
    key = 'auth_created'
    value = {
        'username': pytest.username,
        'email': pytest.email,
        'uuid': str(generate_uuid()),
        'display_name': pytest.display_name,
        'country': pytest.country,
        'status': 'pending'
    }

    events.Auth().handle_event(key=key, data=value)

    accounts = services.AccountService().find()

    assert accounts.total == 1
    account = accounts.items[0]
    assert str(account.user_uuid) == value['uuid']


def test_auth_auth_updated_sync(reset_db, pause_notification, seed_account):
    """
    GIVEN 1 account instance and 1 address in the database
    WHEN directly calling event auth handle_event auth_updated
    THEN it should add 1 account instance and 1 address instance to the database
    """
    key = 'auth_updated'
    value = {
        'username': pytest.username,
        'email': pytest.email,
        'uuid': str(pytest.user_uuid),
        'display_name': pytest.display_name,
        'country': pytest.country,
        'status': 'active'
    }

    events.Auth().handle_event(key=key, data=value)

    accounts = services.AccountService().find()

    assert accounts.total == 1
    account = accounts.items[0]
    assert account.status.name == value['status']
