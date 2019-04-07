import uuid

import us

import pytest
from crosswalk_client import Client
from crosswalk_client.exceptions import (
    BadResponse,
    CreateEntityError,
    MalformedUpdateAttributes,
    UnspecificQueryError,
    EntityNotFoundError,
)


def test_setup(token, service):
    client = Client(token, service)
    client.create_domain("states")


def test_bulk_create(token, service):
    client = Client(token, service)
    domain = client.get_domain("states")
    states = [
        {"name": s.name, "postal_code": s.abbr, "country": "USA"}
        for s in us.states.STATES
    ]
    entities = client.bulk_create(states, domain=domain)
    assert entities[0].name == states[0]["name"]


def test_bulk_create_nested_entity_error(token, service):
    client = Client(token, service, domain="states")
    entities = [{"a": "bad entity", "nested": {"too": "deeply"}}]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities)


def test_bulk_create_entity_with_reserved_attribute_error(token, service):
    client = Client(token, service, domain="states")
    entities = [
        {"a": "bad entity", "created": "with a reserved key, 'created'"}
    ]
    with pytest.raises(CreateEntityError):
        client.bulk_create(entities)


def test_bulk_create_entity_with_uuid(token, service):
    client = Client(token, service, domain="states")
    an_uuid = uuid.uuid4()
    entities = [{"uuid": an_uuid, "name": "an entity with a uuid"}]
    entity = client.bulk_create(entities)[0]
    assert entity.uuid == an_uuid
    entity.delete()


def test_entity_attributes_of_various_types(token, service):
    client = Client(token, service, domain="states")
    entities = [{"real": False, "number": 53, "listicle": [1, "one"]}]
    entity = client.bulk_create(entities)[0]
    assert entity.real is False
    assert entity.number == 53
    assert entity.listicle == [1, "one"]
    entity.delete()


def test_best_match(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match({"name": "Misisipi"})
    assert entity.name == "Mississippi"


def test_best_match_with_block_attrs(token, service):
    client = Client(token, service, domain="states")

    entity = client.best_match(
        {"name": "Arkansas"}, block_attrs={"postal_code": "KS"}
    )
    assert entity.name == "Kansas"

    entity = client.best_match({"name": "Arkansas"})
    assert entity.name == "Arkansas"


def test_match(token, service):
    client = Client(token, service, domain="states")
    entity = client.match(
        {"name": "Kansas"}, block_attrs={"postal_code": "KS"}
    )
    assert entity.name == "Kansas"


def test_match_exceptions(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(UnspecificQueryError):
        client.match({"country": "USA"})
    with pytest.raises(EntityNotFoundError):
        client.match({"country": "Deutschland"})


def test_match_or_create(token, service):
    client = Client(token, service, domain="states")
    entity = client.match_or_create(
        {"name": "Thunderdome"}, create_attrs={"country": "Australia"}
    )
    assert entity.created is True and entity.name == "Thunderdome"

    entity2 = client.match_or_create(
        {"name": "Gas City"}, create_attrs={"country": "Australia"}
    )
    assert entity2.created is True and entity2.name == "Gas City"

    with pytest.raises(UnspecificQueryError):
        client.match_or_create({"country": "Australia"})

    entity.delete()
    entity2.delete()


def test_best_match_or_create(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match_or_create({"name": "Narnia"}, threshold=75)
    assert entity.created is True and entity.name == "Narnia"


def test_best_match_or_create_with_uuid(token, service):
    client = Client(token, service, domain="states")
    an_uuid = uuid.uuid4()
    entity = client.best_match_or_create(
        {"name": "Xanadu"}, create_attrs={"uuid": an_uuid}, threshold=75
    )
    assert entity.uuid == an_uuid


def test_get_entities(token, service):
    client = Client(token, service, domain="states")
    entities = client.get_entities()
    assert entities[0].name is not None


def test_get_entity(token, service):
    client = Client(token, service, domain="states")
    domain = client.get_domain("states")
    entity = client.get_entities(domain=domain)[0]
    returned_entity = client.get_entity(entity.uuid)
    assert returned_entity.uuid == entity.uuid


def test_get_entities_with_block_attrs(token, service):
    client = Client(token, service, domain="states")
    entities = client.get_entities({"country": "USA"})
    assert len(entities) == 51

    entities = client.get_entities({"postal_code": "KS"})
    assert entities[0].name == "Kansas"


def test_update_entity_by_id(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match({"name": "Xanadu"})
    entity = client.update_by_id(
        entity.uuid, {"sacred river": "Alph", "name": "Zanadu"}
    )
    assert entity.name == "Zanadu"
    entity = client.update_by_id(entity.uuid, {"name": "Xanadu"})
    assert entity.sacred_river == "Alph" and entity.name == "Xanadu"


def test_update_entity_by_match(token, service):
    client = Client(token, service, domain="states")
    entity = client.update_match(
        {"name": "Xanadu"}, {"sacred river": "Mississippi"}
    )
    assert entity.sacred_river == "Mississippi"


def test_update_entity_by_match_error(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(UnspecificQueryError):
        client.update_match(
            {"country": "USA"}, {"sacred river": "Mississippi"}
        )


def test_update_entity_by_match_invalid_data_error(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(MalformedUpdateAttributes):
        client.update_match(
            {"name": "Xanadu"}, {"stuff": {"nested": "too deeply"}}
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
    with pytest.raises(UnspecificQueryError):
        client.delete_match({"country": "USA"})


def test_bad_domain_delete_error(token, service):
    client = Client(token, service)
    client.set_domain("countries")  # does not exist
    with pytest.raises(BadResponse):
        client.delete_match({"country": "USA"})


def test_create_or_alias_creates_alias(token, service):
    client = Client(token, service, domain="states")
    entity = client.alias_or_create({"name": "Kalifornia"})
    assert entity.name == "California" and entity.aliased is True


def test_create_or_alias_creates_new(token, service):
    client = Client(token, service, domain="states")
    entity = client.alias_or_create(
        {"name": "Alderaan"},
        create_attrs={"galaxy": "Far, far away"},
        threshold=90,
    )
    assert entity.name == "Alderaan" and entity.aliased is False


def test_create_or_alias_fails_on_existing_entity(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(BadResponse):
        client.alias_or_create(
            {"name": "Alderaan"}, create_attrs={"galaxy": "Far, far away"}
        )


def test_best_match_an_alias(token, service):
    client = Client(token, service, domain="states")
    entity = client.best_match({"name": "Kalifornia"})
    assert entity.name == "California"


def test_cleanup(token, service):
    client = Client(token, service, domain="states")
    for state in us.states.STATES:
        client.delete_match({"name": state.name})
    client.delete_match({"name": "Alderaan"})
    client.delete_domain("states")
