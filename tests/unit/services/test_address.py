import logging
import time

import pytest

from src import services, ManualException
from src.common import time_now
from tests.helpers import generate_uuid

address_service = services.AddressService()


###########
# Find
###########
def test_address_find(reset_db, pause_notification, seed_account, seed_address):
    """
    GIVEN 1 address instance in the database
    WHEN the find method is called
    THEN it should return 1 address
    """

    addresss = address_service.find()
    assert addresss.total == 1
    assert len(addresss.items) == 1
    address = addresss.items[0]
    assert address.uuid == pytest.address.uuid


def test_address_find_by_uuid():
    """
    GIVEN 1 address instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 address
    """
    address = pytest.address
    uuid = address.uuid

    addresss = address_service.find(uuid=uuid)
    assert addresss.total == 1
    assert len(addresss.items) == 1
    address = addresss.items[0]
    assert address.uuid == uuid


def test_address_find_expand_account():
    """
    GIVEN 1 address instance in the database
    WHEN the find method is called with expand argument to also return account
    THEN it should return 1 address
    """
    addresss = address_service.find(expand=['account'])
    assert addresss.total == 1
    assert len(addresss.items) == 1
    address = addresss.items[0]
    assert address.account.uuid is not None


def test_address_find_by_non_existent_column():
    """
    GIVEN 2 address instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 address and ManualException with code 400
    """
    try:
        _ = address_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_address_find_by_non_existent_include():
    """
    GIVEN 2 address instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 address and ManualException with code 400
    """
    try:
        _ = address_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_address_find_by_non_existent_expand():
    """
    GIVEN 2 address instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 address and ManualException with code 400
    """
    try:
        _ = address_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_address_create(reset_db, pause_notification, seed_account):
    """
    GIVEN 1 address instance in the database
    WHEN the create method is called
    THEN it should return 1 address and add 1 address instance into the database
    """
    address = address_service.create(country='CA',
                                     account=pytest.account)

    assert address.uuid is not None
    assert address.country == 'CA'


###########
# Update
###########
def test_address_update(reset_db, pause_notification, seed_account, seed_address):
    """
    GIVEN 2 address instance in the database
    WHEN the update method is called
    THEN it should return 1 address and update 1 address instance into the database
    """
    address = address_service.update(uuid=pytest.address.uuid, country='CA')
    assert address.uuid is not None

    addresss = address_service.find(uuid=address.uuid)
    assert addresss.total == 1
    assert len(addresss.items) == 1
    assert addresss.items[0].country == 'CA'


###########
# Apply
###########
def test_address_apply(reset_db, pause_notification, seed_account, seed_address):
    """
    GIVEN 2 address instance in the database
    WHEN the apply method is called
    THEN it should return 1 address and update 1 address instance in the database
    """
    address = address_service.apply(instance=pytest.address, country='CA')
    assert address.uuid is not None

    addresss = address_service.find(uuid=address.uuid)
    assert addresss.total == 1
    assert len(addresss.items) == 1
