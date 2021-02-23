import json

import pytest

from src import app


#############
# SUCCESS
#############


###########
# Fetch
###########


def test_fetch_account(reset_db, pause_notification, seed_account, seed_address):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'account' is requested
    THEN check that the response is valid
    """
    account_uuid = pytest.account.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/accounts/{account_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    accounts = response['data']['accounts']
    assert accounts['status'] == 'pending'
    assert accounts['uuid'] == str(account_uuid)
    assert accounts['user_uuid'] == str(pytest.user_uuid)
    assert accounts['display_name'] == pytest.display_name
    assert accounts['username'] == pytest.username
    assert accounts['email'] == pytest.email


def test_fetch_account_membership():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'account_membership' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/accounts/membership/{pytest.user_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    membership = response['data']['membership']
    assert membership['status'] == 'pending'
    assert membership['uuid'] == str(pytest.account.uuid)
    assert membership['user_uuid'] == str(pytest.user_uuid)
    assert membership['display_name'] == pytest.display_name
    assert membership['username'] == pytest.username
    assert membership['email'] == pytest.email


###########
# Fetch All
###########


def test_fetch_all_account():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'accounts' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Request
    response = app.test_client().get(f'/accounts',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['accounts']) == 1
    accounts = response['data']['accounts'][0]
    assert accounts['status'] == 'pending'
    assert accounts['uuid'] == str(pytest.account.uuid)
    assert accounts['user_uuid'] == str(pytest.user_uuid)
    assert accounts['display_name'] == pytest.display_name
    assert accounts['username'] == pytest.username
    assert accounts['email'] == pytest.email


def test_fetch_all_account_bulk():
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'accounts_bulk' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {
        'within': {
            'key': 'user_uuid',
            'value': [str(pytest.user_uuid)]
        }
    }

    # Request
    response = app.test_client().post(f'/accounts/bulk',
                                      headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['accounts']) == 1
    accounts = response['data']['accounts'][0]
    assert accounts['status'] == 'pending'
    assert accounts['uuid'] == str(pytest.account.uuid)
    assert accounts['user_uuid'] == str(pytest.user_uuid)
    assert accounts['display_name'] == pytest.display_name
    assert accounts['username'] == pytest.username
    assert accounts['email'] == pytest.email


###########
# Update
###########


def test_update_account(pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'account' is requested
    THEN check that the response is valid
    """
    account_uuid = pytest.account.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'display_name': 'Oingo Boingo'}

    # Request
    response = app.test_client().put(f'/accounts/{account_uuid}',
                                     headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    accounts = response['data']['accounts']
    assert accounts['status'] == 'pending'
    assert accounts['uuid'] == str(account_uuid)
    assert accounts['user_uuid'] == str(pytest.user_uuid)
    assert accounts['display_name'] == 'Oingo Boingo'
    assert accounts['username'] == pytest.username
    assert accounts['email'] == pytest.email


#############
# FAIL
#############

###########
# Update
###########

def test_account_update_fail(reset_db, pause_notification, seed_account, seed_address):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'account' is requested
    THEN check that the response is valid
    """
    account_uuid = pytest.account.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.user_uuid}

    # Payload
    payload = {'address': 'junk'}

    # Request
    response = app.test_client().put(f'/accounts/{account_uuid}',
                                     headers=headers, json=payload)

    # Response
    assert response.status_code == 400
