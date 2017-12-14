import uuid

import pytest
import us

from crosswalk_client import Client
from crosswalk_client.exceptions import (BadResponse, CreateEntityError,
                                         UnspecificDeleteRequestError,
                                         UnspecificUpdateRequestError,
                                         UpdateEntityError)


def test_setup(token, service):
    client = Client(token, service)
    client.create_domain("states")


def test_bulk_create(token, service):
    client = Client(token, service, domain="states")
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
    entities = client.bulk_create(states)
    assert entities[0].name == states[0]["name"]


def test_bulk_create_nested_entity_error(token, service):
    client = Client(token, service, domain="states")
    entities = [
        {
            "a": "bad entity",
            "nested": {
                "too": "deeply"
            }
        }
    ]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities)


def test_bulk_create_entity_with_reserved_attribute_error(token, service):
    client = Client(token, service, domain="states")
    entities = [
        {
            "a": "bad entity",
            "created": "with a reserved key, 'created'"
        }
    ]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities)


def test_best_match(token, service):
    client = Client(token, service)
    entity = client.best_match({"name": "Misisipi"}, domain="states")
    assert entity.name == "Mississippi"


def test_best_match_with_block_attrs(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match(
        {"name": "Arkansas"},
        block_attrs={"postal_code": "KS"},
    )
    assert entity.name == "Kansas"

    entity = client.best_match({"name": "Arkansas"})
    assert entity.name == "Arkansas"


def test_best_match_or_create(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match_or_create(
        {"name": "Narnia"},
        threshold=75,
    )
    assert entity.created is True


def test_best_match_or_create_with_uuid(token, service):
    client = Client(token, service, domain="states")
    an_uuid = uuid.uuid4().hex
    entity = client.best_match_or_create(
        {"name": "Xanadu"},
        create_attrs={"uuid": an_uuid},
        threshold=75,
    )
    assert entity.uuid == an_uuid


def test_get_entities(token, service):
    client = Client(token, service, domain="states")
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
    client = Client(token, service, domain="states")
    entity = client.best_match({"name": "Xanadu"})
    response = client.delete_by_id(entity.uuid)
    assert response is True


def test_unspecific_delete_error(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(UnspecificDeleteRequestError):
        client.delete_match({"country": "USA"})


def test_bad_domain_delete_error(token, service):
    client = Client(token, service)
    client.set_domain("countries")  # does not exist
    with pytest.raises(BadResponse):
        client.delete_match({"country": "USA"})


def test_create_alias(token, service):
    client = Client(token, service, domain="states")
    entity = client.create_matched_alias(
        {"name": "Kalifornia"},
        create_attrs={
            "side": "west"
        },
        threshold=80
    )
    assert entity.name == "California"


def test_create_alias_without_match_error(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(CreateEntityError):
        client.create_matched_alias(
            {"name": "Zanado"},
            threshold=80,
        )


def test_best_match_alias(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match({"name": "Kalifornia"})
    assert entity.name == "California"


def test_cleanup(token, service):
    client = Client(token, service, domain="states")
    for state in us.states.STATES:
        client.delete_match({"name": state.name})
    client.delete_domain("states")
