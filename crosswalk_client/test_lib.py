import pytest
import requests
import us

from crosswalk_client import Client

from .exceptions import ConfigError, ProtectedError


def test_misconfigured_config(token, service):
    with pytest.raises(ConfigError):
        Client('NOTATOKEN', service)


def test_properly_configured_config(token, service):
    client = Client(token, service)
    response = client.client_check()
    assert response.status_code == requests.codes.ok


def test_create_domain(token, service):
    client = Client(token, service)
    response = client.create_domain('states')
    assert response['name'] == 'states'

    response = client.create_domain('counties', parent="states")
    assert response['name'] == 'counties'


def test_list_domains(token, service):
    client = Client(token, service)
    entities = client.list_domains()
    assert entities == [
        {
            "slug": "states",
            "name": "states",
            "parent": None
        },
        {
            "slug": "counties",
            "name": "counties",
            "parent": "states"
        },
    ]


def test_delete_domain(token, service):
    client = Client(token, service)
    response = client.delete_domain('counties')
    assert response.status_code == 204


def test_delete_protected_domain(token, service):
    with pytest.raises(ProtectedError):
        client = Client(token, service)
        client.delete_domain('states')


def test_best_match(token, service):
    client = Client(token, service)
    client.set_domain('states')
    response = client.best_match({"name": "Mississipi"})
    print(response)
    assert response['entity']['attributes']['name'] == "Mississippi"


def test_best_match_with_matched_attrs(token, service):
    client = Client(token, service)
    client.set_domain('states')
    response = client.best_match(
        {"name": "Arkansas"},
        {"postal_code": "KS"}
    )
    assert response['entity']['attributes']['name'] == "Kansas"

    response = client.best_match({"name": "Arkansas"})
    assert response['entity']['attributes']['name'] == "Arkansas"


def test_best_match_or_create(token, service):
    client = Client(token, service)
    client.set_domain('states')
    response = client.best_match_or_create(
        {"name": "Narnia"}, create_threshold=75)
    assert response['created'] is True

# def test_bulk_create(token, service):
#     client = Client(token, service)
#     states = [
#         {
#             "name": s.name,
#             "ap_abbreviation": s.ap_abbr,
#             "fips": s.fips,
#             "postal_code": s.abbr
#         }
#         for s in us.states.STATES
#     ]
#     response = client.bulk_create('states', states)
#     assert response.status_code == requests.codes.ok
