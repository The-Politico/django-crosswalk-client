import pytest
from crosswalk_client import Client
from crosswalk_client.exceptions import (
    MalformedBlockAttributes,
    MalformedDomain,
    MalformedQuery,
    MalformedThreshold,
    MalformedUUID,
    MissingDomain,
)


def test_validate_query_not_a_dictionary(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(MalformedQuery):
        client.alias_or_create("test")


def test_validate_query_too_many_query_fields(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(MalformedQuery):
        client.alias_or_create({"name": "Alderaan", "galaxy": "Far, far away"})


def test_validate_query_query_not_a_string(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(MalformedQuery):
        client.alias_or_create({"name": 1})


def test_validate_domain_missing(token, service):
    client = Client(token, service)
    with pytest.raises(MissingDomain):
        client.get_entities()


def test_validate_domain_not_a_slug(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedDomain):
        client.get_entities(domain="NotASlug")


def test_validate_domain_not_a_string(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedDomain):
        client.get_entities(domain=123)


def validate_block_attrs_not_a_dictionary(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedBlockAttributes):
        client.best_match({"name": "entity"}, block_attrs="not a dictionary")


def validate_block_attrs_nested(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedBlockAttributes):
        client.best_match(
            {"name": "entity"}, block_attrs={"nested": {"too": "deep"}}
        )


def test_validate_uuid_malformed(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedUUID):
        client.delete_by_id("2bc1c94f 0deb-43e9-92a1-4775189ec9f8")


def test_validate_threshold_not_an_integer(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedThreshold):
        client.best_match_or_create(
            {"name": "Xanadu"}, domain="domain", threshold="bad"
        )


def test_validate_threshold_out_of_range(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedThreshold):
        client.best_match_or_create(
            {"name": "Xanadu"}, domain="domain", threshold=200
        )
