import time

import pytest

from src import services


def test_account_notification_account_active(reset_db, kafka_conn_last_msg):
    pytest.account = services.AccountService().create(status='active', role='member', user_uuid=pytest.user_uuid,
                                                      email=pytest.email, display_name=pytest.display_name,
                                                      username=pytest.username)
    time.sleep(1)
    msg = kafka_conn_last_msg('accounts')
    assert msg.key is not None
    assert msg.key == 'account_active'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.account.uuid)


def test_account_notification_account_inactive(reset_db, kafka_conn_last_msg):
    pytest.account = services.AccountService().create(status='inactive', role='member', user_uuid=pytest.user_uuid,
                                                      email=pytest.email, display_name=pytest.display_name,
                                                      username=pytest.username)
    time.sleep(1)
    msg = kafka_conn_last_msg('accounts')
    assert msg.key is not None
    assert msg.key == 'account_inactive'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.account.uuid)


def test_account_notification_account_pending(reset_db, kafka_conn_last_msg):
    pytest.account = services.AccountService().create(status='pending', role='member', user_uuid=pytest.user_uuid,
                                                      email=pytest.email, display_name=pytest.display_name,
                                                      username=pytest.username)
    time.sleep(1)
    msg = kafka_conn_last_msg('accounts')
    assert msg.key is not None
    assert msg.key == 'account_pending'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.account.uuid)


def test_account_notification_account_active_update(reset_db, kafka_conn_last_msg, seed_account):
    pytest.account = services.AccountService().update(uuid=pytest.account.uuid, status='inactive')
    time.sleep(1)
    msg = kafka_conn_last_msg('accounts')
    assert msg.key is not None
    assert msg.key == 'account_inactive'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.account.uuid)


def test_account_notification_display_name_updated(reset_db, kafka_conn_last_msg, seed_account):
    pytest.account = services.AccountService().update(uuid=pytest.account.uuid, display_name='Baby D')
    time.sleep(1)
    msg = kafka_conn_last_msg('accounts')
    assert msg.key is not None
    assert msg.key == 'display_name_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.account.uuid)
    assert msg.value['display_name'] == 'Baby D'
