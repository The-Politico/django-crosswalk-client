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


def test_set_threshold(token, service):
    client = Client(token, service)
    client.set_threshold(99)
    assert client.threshold == 99


def test_set_domain(token, service):
    client = Client(token, service)
    client.set_domain("sharks")
    assert client.domain == "sharks"


def test_set_scorer(token, service):
    client = Client(token, service)
    client.set_scorer("random.scorer")
    assert client.scorer == "random.scorer"
