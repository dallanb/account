import pytest

from src import services
from src.common import DB, Cleaner
from src.models import *
from tests.helpers import generate_uuid

db = DB()
cleaner = Cleaner()


def test_init(reset_db):
    """
    GIVEN a db instance
    WHEN calling the init method of the db instance on the Address model
    THEN it should return the address instance
    """
    instance = db.init(model=Address, country='CA')
    assert cleaner.is_mapped(instance) == instance
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.country == 'CA'

    db.rollback()


def test_count():
    """
    GIVEN a db instance
    WHEN calling the count method of the db instance on the Address model
    THEN it should return the number of address instances
    """
    count = db.count(model=Address)
    assert count == 0

    address = db.init(model=Address, country='CA')
    _ = db.save(instance=address)
    count = db.count(model=Address)
    assert count == 1


def test_add(reset_db):
    """
    GIVEN a db instance
    WHEN calling the add method of the db instance on a address instance
    THEN it should add a address instance to the database
    """
    instance = db.init(model=Address, country='CA')
    address = db.add(instance=instance)
    assert cleaner.is_uuid(address.uuid) is not None
    assert address.country == 'CA'

    db.rollback()
    assert db.count(model=Address) == 0


def test_commit(reset_db):
    """
    GIVEN a db instance
    WHEN calling the commit method of the db instance on a address instance
    THEN it should add a address instance to the database
    """
    instance = db.init(model=Address, country='CA')
    address = db.add(instance=instance)
    assert cleaner.is_uuid(address.uuid) is not None
    assert address.country == 'CA'

    db.rollback()
    assert db.count(model=Address) == 0

    _ = db.add(instance=instance)
    db.commit()
    assert db.count(model=Address) == 1

    instance_0 = db.init(model=Address, country='CA')
    instance_1 = db.init(model=Address, country='CA')
    instance_2 = db.init(model=Address, country='CA')
    db.add(instance=instance_0)
    db.add(instance=instance_1)
    db.add(instance=instance_2)
    db.commit()
    assert db.count(model=Address) == 4


def test_save(reset_db):
    """
    GIVEN a db instance
    WHEN calling the save method of the db instance on a address instance
    THEN it should add a address instance to the database
    """
    instance = db.init(model=Address, country='CA')
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.country == 'CA'
    address = db.save(instance=instance)
    assert db.count(model=Address) == 1
    assert address.country == 'CA'


def test_find():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance
    THEN it should find a address instance from the database
    """
    result = db.find(model=Address)
    assert result.total == 1
    assert len(result.items) == 1

    result = db.find(model=Address, uuid=generate_uuid())
    assert result.total == 0


def test_destroy():
    """
    GIVEN a db instance
    WHEN calling the destroy method of the db instance on a address instance
    THEN it should remove the address instance from the database
    """
    result = db.find(model=Address)
    assert result.total == 1
    assert len(result.items) == 1
    instance = result.items[0]

    assert db.destroy(instance=instance)
    assert db.count(model=Address) == 0


def test_rollback(reset_db):
    """
    GIVEN a db instance
    WHEN calling the rollback method of the db instance
    THEN it should rollback a address instance from being inserted the database
    """
    instance = db.init(model=Address, country='CA')
    db.rollback()
    db.commit()
    assert db.count(model=Address) == 0

    instance = db.init(model=Address, country='CA')
    db.save(instance=instance)
    db.rollback()
    assert db.count(model=Address) == 1


def test_clean_query(reset_db):
    """
    GIVEN a db instance
    WHEN calling the clean_query method of the db instance
    THEN it should return a query
    """
    query = db.clean_query(model=Address)
    assert query is not None


def test_run_query(reset_db, pause_notification, seed_account, seed_address):
    """
    GIVEN a db instance
    WHEN calling the run_query method of the db instance with a valid query
    THEN it should return the query result
    """
    query = db.clean_query(model=Address)
    address = db.run_query(query=query)
    assert address.total == 1


def test_equal_filter():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with an equal filter
    THEN it should return the query result
    """
    country = 'CA'
    address = db.find(model=Address, country=country)
    assert address.total == 1

    address = db.find(model=Address, country=country, uuid=pytest.address.uuid)
    assert address.items[0] == pytest.address


def test_nested_filter(reset_db, pause_notification, seed_account, seed_address):
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a nested filter
    THEN it should return the query result
    """
    address = db.find(model=Address, nested={'account': {'uuid': pytest.account.uuid}})
    assert address.total == 1


def test_within_filter():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a within filter
    THEN it should return the query result
    """

    address = db.find(model=Address)
    assert address.total == 1

    address = db.find(model=Address, within={'uuid': [pytest.address.uuid]})
    assert address.total == 1

# def test_has_key_filter():
#     """
#     GIVEN a db instance
#     WHEN calling the find method of the db instance with a has_key filter
#     THEN it should return the query result
#     """
#     
#
#     address = db.find(model=Address)
#     assert address.total == 2
#
#     address = db.find(model=Address, has_key={'uuid': global_address.uuid})
#     assert address.total == 0
