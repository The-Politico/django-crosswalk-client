import pytest

from crosswalk_client import Client
from crosswalk_client.exceptions import ProtectedDomainError


def test_create_domain(token, service):
    client = Client(token, service)
    domain = client.create_domain("states")
    assert domain.name == "states"

    domain = client.create_domain("counties", parent="states")
    assert domain.name == "counties" and domain.parent == "states"


def test_update_domain(token, service):
    client = Client(token, service)
    domain = client.update_domain(
        "counties",
        {"name": "kounties", "parent": None}
    )
    assert domain.name == "kounties" and domain.parent is None


def test_get_domain(token, service):
    client = Client(token, service)
    domain = client.get_domain("states")
    assert domain.slug == "states"


def test_get_domains(token, service):
    client = Client(token, service)
    domains = client.get_domains()
    assert domains[0].slug == "states"


def test_delete_protected_domain_error(token, service):
    client = Client(token, service)
    client.bulk_create([{"name": "Kansas"}], domain="states")
    with pytest.raises(ProtectedDomainError):
        client.delete_domain("states")


def test_delete_domain(token, service):
    client = Client(token, service)
    response = client.delete_domain("counties")
    assert response is True


def test_cleanup(token, service):
    client = Client(token, service, domain="states")
    client.delete_match({"name": "Kansas"})
    client.delete_domain("states")
