import pytest

from crosswalk_client import Client
from crosswalk_client.exceptions import ConfigError


def test_misconfigured_config(token, service):
    with pytest.raises(ConfigError):
        Client('NOTAVALIDTOKEN', service)


def test_properly_configured_config(token, service):
    client = Client(token, service)
    response = client.client_check()
    assert response is True
