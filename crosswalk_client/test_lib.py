import requests

import pytest
from crosswalk_client import Client

from .exceptions import ConfigError


def test_misconfigured_config(token, service):
    with pytest.raises(ConfigError):
        Client('NOTATOKEN', service)


def test_properly_configured_config(token, service):
    client = Client(token, service)
    assert client.client_check() == requests.codes.ok
