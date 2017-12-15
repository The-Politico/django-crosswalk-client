import pytest

from crosswalk_client import Client
from crosswalk_client.exceptions import MalformedQuery, MissingDomain


def test_validate_query_not_a_dictionary(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(MalformedQuery):
        client.alias_or_create('test')


def test_validate_query_too_many_query_fields(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(MalformedQuery):
        client.alias_or_create(
            {"name": "Alderaan", "galaxy": "Far, far away"}
        )


def test_validate_query_query_not_a_string(token, service):
    client = Client(token, service, domain="states")
    with pytest.raises(MalformedQuery):
        client.alias_or_create({"name": 1})


def test_validate_missing_domain(token, service):
    client = Client(token, service)
    with pytest.raises(MissingDomain):
        client.get_entities()
