import pytest

from src import services, ManualException, app
from tests.helpers import generate_uuid

account_service = services.AccountService()


###########
# Find
###########
def test_account_find(reset_db, pause_notification, seed_account):
    """
    GIVEN 1 account instance in the database
    WHEN the find method is called
    THEN it should return 1 account
    """

    accounts = account_service.find()
    assert accounts.total == 1
    assert len(accounts.items) == 1
    account = accounts.items[0]
    assert account.uuid == pytest.account.uuid


def test_account_find_by_uuid():
    """
    GIVEN 1 account instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 account
    """
    account = pytest.account
    uuid = account.uuid

    accounts = account_service.find(uuid=uuid)
    assert accounts.total == 1
    assert len(accounts.items) == 1
    account = accounts.items[0]
    assert account.uuid == uuid


def test_account_find_by_user_uuid():
    """
    GIVEN 1 account instance in the database
    WHEN the find method is called with user_uuid
    THEN it should return 1 account
    """
    account = pytest.account
    user_uuid = account.user_uuid

    accounts = account_service.find(user_uuid=user_uuid)
    assert accounts.total == 1
    assert len(accounts.items) == 1
    account = accounts.items[0]
    assert account.user_uuid == user_uuid


def test_account_find_include_address(pause_notification, seed_address):
    """
    GIVEN 1 account instance in the database
    WHEN the find method is called with include argument to also return address
    THEN it should return 1 account
    """
    accounts = account_service.find(include=['address'])
    assert accounts.total == 1
    assert len(accounts.items) == 1
    account = accounts.items[0]
    assert account.address is not None


def test_account_find_w_pagination(pause_notification):
    """
    GIVEN 2 account instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of accounts defined in the pagination arguments
    """
    account_service.create(status='pending', role='member', user_uuid=generate_uuid(),
                           email='babyd@sfu.ca', display_name='Baby D',
                           username='babyd')

    accounts_0 = account_service.find(page=1, per_page=1)
    assert accounts_0.total == 2
    assert len(accounts_0.items) == 1

    accounts_1 = account_service.find(page=2, per_page=1)
    assert accounts_1.total == 2
    assert len(accounts_1.items) == 1
    assert accounts_1.items[0] != accounts_0.items[0]

    accounts = account_service.find(page=1, per_page=2)
    assert accounts.total == 2
    assert len(accounts.items) == 2


def test_account_find_w_bad_pagination():
    """
    GIVEN 2 account instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 account
    """
    accounts = account_service.find(page=3, per_page=3)
    assert accounts.total == 2
    assert len(accounts.items) == 0


def test_account_find_by_user_uuid_none_found():
    """
    GIVEN 2 account instance in the database
    WHEN the find method is called with a random user_uuid
    THEN it should return the 0 account
    """
    accounts = account_service.find(user_uuid=generate_uuid())
    assert accounts.total == 0
    assert len(accounts.items) == 0


def test_account_find_by_non_existent_column():
    """
    GIVEN 2 account instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 account and ManualException with code 400
    """
    try:
        _ = account_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_account_find_by_non_existent_include():
    """
    GIVEN 2 account instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 account and ManualException with code 400
    """
    try:
        _ = account_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_account_find_by_non_existent_expand():
    """
    GIVEN 2 account instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 account and ManualException with code 400
    """
    try:
        _ = account_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_account_create(reset_db, pause_notification):
    """
    GIVEN 0 account instance in the database
    WHEN the create method is called
    THEN it should return 1 account and add 1 account instance into the database
    """
    account = account_service.create(status='pending', role='member', user_uuid=pytest.user_uuid,
                                     email=pytest.email, display_name=pytest.display_name,
                                     username=pytest.username)

    assert account.uuid is not None
    assert account.user_uuid == pytest.user_uuid


def test_account_create_dup(pause_notification):
    """
    GIVEN 1 account instance in the database
    WHEN the create method is called with the exact same parameters of an existing account
    THEN it should return 0 account and add 0 account instance into the database and ManualException with code 500
    """
    try:
        _ = account_service.create(status='pending', role='member', user_uuid=pytest.user_uuid,
                                   email=pytest.email, display_name=pytest.display_name,
                                   username=pytest.username)
    except ManualException as ex:
        assert ex.code == 500


def test_account_create_w_bad_field(pause_notification):
    """
    GIVEN 1 account instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 account and add 0 account instance into the database and ManualException with code 500
    """
    try:
        _ = account_service.create(status='pending', role='member', user_uuid=generate_uuid(),
                                   email='babyd@sfu.ca', display_name='Baby D',
                                   username='babyd', junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_account_update(reset_db, pause_notification, seed_account):
    """
    GIVEN 1 account instance in the database
    WHEN the update method is called
    THEN it should return 1 account and update 1 account instance into the database
    """
    account = account_service.update(uuid=pytest.account.uuid, display_name='Baby D')
    assert account.uuid is not None

    accounts = account_service.find(uuid=account.uuid)
    assert accounts.total == 1
    assert len(accounts.items) == 1


def test_account_update_w_bad_uuid(reset_db, pause_notification, seed_account):
    """
    GIVEN 1 account instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 account and update 0 account instance into the database and ManualException with code 404
    """
    try:
        _ = account_service.update(uuid=generate_uuid(), display_name='Baby D')
    except ManualException as ex:
        assert ex.code == 404


def test_account_update_w_bad_field(pause_notification):
    """
    GIVEN 1 account instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 account and update 0 account instance in the database and ManualException with code 400
    """
    try:
        _ = account_service.update(uuid=pytest.account.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_account_apply(reset_db, pause_notification, seed_account):
    """
    GIVEN 1 account instance in the database
    WHEN the apply method is called
    THEN it should return 1 account and update 1 account instance in the database
    """
    account = account_service.apply(instance=pytest.account, display_name='Baby D')
    assert account.uuid is not None

    accounts = account_service.find(uuid=account.uuid)
    assert accounts.total == 1
    assert len(accounts.items) == 1


def test_account_apply_w_bad_account(reset_db, pause_notification, seed_account):
    """
    GIVEN 1 account instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 account and update 0 account instance in the database and ManualException with code 404
    """
    try:
        _ = account_service.apply(instance=generate_uuid(), display_name='Baby D')
    except ManualException as ex:
        assert ex.code == 400


def test_account_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 account instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 account and update 0 account instance in the database and ManualException with code 400
    """
    try:
        _ = account_service.apply(instance=pytest.account, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_generate_mail(reset_db, pause_notification,
                       seed_account):
    """
    GIVEN 1 account instance in the database
    WHEN the generate_mail method is called
    THEN it should return a mail obj ready to be sent by our mail library
    """
    with app.app_context():
        mail = account_service.generate_mail(uuid=pytest.account.uuid, type='register')
    assert 'to' in mail
    assert 'subject' in mail
    assert 'html' in mail
