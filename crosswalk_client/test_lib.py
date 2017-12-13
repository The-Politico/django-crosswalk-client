import uuid

import pytest
import us

from crosswalk_client import Client

from .exceptions import (BadResponse, ConfigError, CreateEntityError,
                         ProtectedDomainError, UnspecificDeleteRequestError,
                         UnspecificUpdateRequestError, UpdateEntityError)


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


def test_get_domains(token, service):
    client = Client(token, service)
    domains = client.get_domains()
    assert domains[0].slug == "states"


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
    entities = client.bulk_create(states, domain='states')
    assert entities[0].name == states[0]['name']


def test_bulk_create_nested_entity_error(token, service):
    client = Client(token, service)
    entities = [
        {
            "a": "bad entity",
            "nested": {
                "too": "deeply"
            }
        }
    ]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities, domain='states')


def test_bulk_create_entity_with_reserved_attribute_error(token, service):
    client = Client(token, service)
    entities = [
        {
            "a": "bad entity",
            "created": "with a reserved key, 'created'"
        }
    ]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities, domain='states')


def test_delete_domain(token, service):
    client = Client(token, service)
    response = client.delete_domain('counties')
    assert response is True


def test_delete_protected_domain_error(token, service):
    with pytest.raises(ProtectedDomainError):
        client = Client(token, service)
        client.delete_domain('states')


def test_best_match(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match({"name": "Misisipi"})
    assert entity.name == "Mississippi"


def test_best_match_with_block_attrs(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match(
        {"name": "Arkansas"},
        block_attrs={"postal_code": "KS"},
    )
    assert entity.name == "Kansas"

    entity = client.best_match({"name": "Arkansas"})
    assert entity.name == "Arkansas"


def test_best_match_or_create(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match_or_create(
        {"name": "Narnia"},
        create_threshold=75,
    )
    assert entity.created is True


def test_best_match_or_create_with_uuid(token, service):
    client = Client(token, service)
    client.set_domain('states')
    an_uuid = uuid.uuid4().hex
    entity = client.best_match_or_create(
        {"name": "Xanadu"},
        create_attrs={"uuid": an_uuid},
        create_threshold=75,
    )
    assert entity.uuid == an_uuid


def test_get_entities(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entities = client.get_entities()
    assert entities[0].name is not None


def test_update_entity_by_id(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match({"name": "Xanadu"})
    entity = client.update_by_id(
        entity.uuid,
        {"sacred river": "Alph", "name": "Zanadu"}
    )
    entity = client.update_by_id(entity.uuid, {"name": "Xanadu"})
    assert entity.sacred_river == "Alph" and entity.name == "Xanadu"


def test_update_entity_by_match(token, service):
    client = Client(token, service, domain="states")
    entity = client.update_match(
        {"name": "Xanadu"},
        {"sacred river": "Mississippi"}
    )
    assert entity.sacred_river == "Mississippi"


def test_update_entity_by_match_error(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(UnspecificUpdateRequestError):
        client.update_match(
            {"country": "USA"},
            {"sacred river": "Mississippi"}
        )


def test_update_entity_by_match_invalid_data_error(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(UpdateEntityError):
        client.update_match(
            {"name": "Xanadu"},
            {"stuff": {"nested": "too deeply"}}
        )


def test_delete_entity_by_match(token, service):
    client = Client(token, service, domain="states")
    deleted = client.delete_match({"name": "Narnia"})
    assert deleted is True


def test_delete_entity_by_id(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match({"name": "Xanadu"})
    response = client.delete_by_id(entity.uuid)
    assert response is True


def test_unspecific_delete_error(token, service):
    client = Client(token, service)
    client.set_domain('states')
    with pytest.raises(UnspecificDeleteRequestError):
        client.delete_match({"country": "USA"})


def test_bad_domain_delete_error(token, service):
    client = Client(token, service)
    client.set_domain('countries')
    with pytest.raises(BadResponse):
        client.delete_match({"country": "USA"})


def test_create_alias(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.create_matched_alias(
        {'name': 'Kalifornia'},
        create_attrs={
            "side": "west"
        },
        create_threshold=80
    )
    assert entity.name == 'California'


def test_create_alias_without_match_error(token, service):
    client = Client(token, service)
    client.set_domain('states')
    with pytest.raises(CreateEntityError):
        client.create_matched_alias(
            {'name': 'Zanado'},
            create_threshold=80,
        )


def test_best_match_alias(token, service):
    client = Client(token, service)
    client.set_domain('states')
    entity = client.best_match({"name": "Kalifornia"})
    assert entity.name == "California"


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
