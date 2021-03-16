import logging

import pytest
import time

from src import services


def test_address_notification_country_updated(reset_db, kafka_conn_last_msg, seed_account):
    address = services.AddressService().create(account=pytest.account, country=pytest.country)
    _ = services.AddressService().update(uuid=address.uuid, country='US')
    time.sleep(0.2)
    msg = kafka_conn_last_msg('accounts')
    assert msg.key is not None
    assert msg.key == 'country_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.account.uuid)
    assert msg.value['country'] == 'US'
