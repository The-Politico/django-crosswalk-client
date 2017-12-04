import requests

import pytest
import us
from crosswalk_client import Client

from .exceptions import ConfigError


def test_misconfigured_config(token, service):
    with pytest.raises(ConfigError):
        Client('NOTATOKEN', service)


def test_properly_configured_config(token, service):
    client = Client(token, service)
    response = client.client_check()
    assert response.status_code == requests.codes.ok


def test_create_domain(token, service):
    client = Client(token, service)
    domain = client.create_domain('states')
    assert domain['name'] == 'states'


def test_bulk_create(token, service):
    client = Client(token, service)
    states = [
        {
            "name": s.name,
            "ap_abbreviation": s.ap_abbr,
            "fips": s.fips,
            "postal_code": s.abbr
        }
        for s in us.states.STATES
    ]
    response = client.bulk_create('states', states)
    assert response.status_code == requests.codes.ok


def test_delete_domain(token, service):
    client = Client(token, service)
    response = client.delete_domain('states')
    assert response.status_code == requests.codes.ok
