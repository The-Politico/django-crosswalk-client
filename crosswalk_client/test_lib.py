import pytest
import us

from crosswalk_client import Client

from .exceptions import (BadResponse, ConfigError, CreateEntityError,
                         ProtectedDomainError, UnspecificDeleteRequestError)


def test_misconfigured_config(token, service):
    with pytest.raises(ConfigError):
        Client('NOTATOKEN', service)


def test_properly_configured_config(token, service):
    client = Client(token, service)
    response = client.client_check()
    assert response is True


def test_create_domain(token, service):
    client = Client(token, service)
    response = client.create_domain('states')
    assert response.name == 'states'

    response = client.create_domain('counties', parent="states")
    assert response.name == 'counties'


def test_list_domains(token, service):
    client = Client(token, service)
    entities = client.list_domains()
    assert entities[0].slug == "states"


def test_bulk_create(token, service):
    client = Client(token, service)
    states = [
        {
            "name": s.name,
            "ap_abbreviation": s.ap_abbr,
            "fips": s.fips,
            "postal_code": s.abbr,
            "country": "USA"
        }
        for s in us.states.STATES
    ]
    response = client.bulk_create(states, domain='states')
    assert response is True


def test_bulk_create_nested_entity(token, service):
    client = Client(token, service)
    entities = [
        {
            "a": "bad entity",
            "nested": {
                "too": "deep"
            }
        }
    ]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities, domain='states')


def test_bulk_create_entity_with_reserved_attribute(token, service):
    client = Client(token, service)
    entities = [
        {
            "a": "bad entity",
            "created": "with a reserved key"
        }
    ]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities, domain='states')


def test_delete_domain(token, service):
    client = Client(token, service)
    response = client.delete_domain('counties')
    assert response is True


def test_delete_protected_domain(token, service):
    with pytest.raises(ProtectedDomainError):
        client = Client(token, service)
        client.delete_domain('states')


def test_best_match(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match({"name": "Mississipi"})
    assert entity.name == "Mississippi"


def test_best_match_with_matched_attrs(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match(
        {"name": "Arkansas"},
        {"postal_code": "KS"}
    )
    assert entity.name == "Kansas"

    entity = client.best_match({"name": "Arkansas"})
    assert entity.name == "Arkansas"


def test_best_match_or_create(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match_or_create(
        {"name": "Narnia"}, create_threshold=75)
    assert entity.created is True


def test_delete(token, service):
    client = Client(token, service)
    client.set_domain('states')
    deleted = client.delete_match({"name": "Narnia"})
    assert deleted is True


def test_unspecific_delete(token, service):
    client = Client(token, service)
    client.set_domain('states')
    with pytest.raises(UnspecificDeleteRequestError):
        client.delete_match({"country": "USA"})


def test_bad_domain_delete(token, service):
    client = Client(token, service)
    client.set_domain('countries')
    with pytest.raises(BadResponse):
        client.delete_match({"country": "USA"})


def test_cleanup_entities(token, service):
    client = Client(token, service)
    client.set_domain('states')
    for state in us.states.STATES:
        response = client.delete_match({"name": state.name})
    assert response is True


def test_cleanup_domains(token, service):
    client = Client(token, service)
    client.set_domain('states')
    response = client.delete_domain('states')
    assert response is True
