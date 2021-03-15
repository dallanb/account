import pytest

from src import services


@pytest.fixture(scope="function")
def seed_address():
    pytest.address = services.AddressService().create(country=pytest.country, account=pytest.account)
