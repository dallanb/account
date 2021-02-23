from uuid import uuid4

import pytest

from .fixtures import *


def pytest_configure(config):
    pytest.account = None
    pytest.address = None
    pytest.user_uuid = uuid4()
    pytest.email = 'dallanbhatti@gmail.com'
    pytest.display_name = 'Dallan Bhatti'
    pytest.username = 'dallanbhatti'
    pytest.country = 'CA'
