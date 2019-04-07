import pytest
from crosswalk_client import Client
from crosswalk_client.exceptions import (
    MalformedDomain,
    MissingDomain,
    ProtectedDomainError,
)


def test_create_domain(token, service):
    client = Client(token, service)
    states = client.create_domain("states")
    assert states.name == "states"

    counties = client.create_domain("counties", parent="states")
    assert counties.name == "counties" and counties.parent == "states"

    cities = client.create_domain("cities", parent=states)
    assert cities.name == "cities" and cities.parent == "states"

    with pytest.raises(MalformedDomain):
        client.create_domain(1)

    with pytest.raises(MalformedDomain):
        client.create_domain("townships", parent=1)

    townships = client.create_domain("townships", parent=states)
    assert townships.name == "townships" and townships.parent == "states"


def test_create_domain_exceptions(token, service):
    client = Client(token, service)
    with pytest.raises(MissingDomain):
        client.create_domain()
    with pytest.raises(MalformedDomain):
        client.create_domain("countries", parent="a parent name")
    with pytest.raises(MalformedDomain):
        client.create_domain("countries", parent=1)


def test_update_domain(token, service):
    client = Client(token, service)
    # Client passed slug
    domain = client.update_domain(
        "counties", {"name": "kounties", "parent": None}
    )
    assert domain.name == "kounties" and domain.parent is None
    # Client passed instance
    domain = client.update_domain(domain, {"name": "counties", "parent": None})
    assert domain.name == "counties"
    # Instance method
    domain.update({"name": "kounties"})
    assert domain.name == "kounties"
    # Exception
    with pytest.raises(MalformedDomain):
        client.update_domain(1, {"name": "counties"})


def test_get_domain(token, service):
    client = Client(token, service)
    domain = client.get_domain("states")
    assert domain.slug == "states"

    with pytest.raises(MalformedDomain):
        client.get_domain(1)


def test_get_domains(token, service):
    client = Client(token, service)
    domains = client.get_domains()
    states = domains[0]
    assert states.slug == "states"

    domains = client.get_domains(parent=states)
    assert len(domains) == 2

    domains = client.get_domains(parent="states")
    assert len(domains) == 2


def test_get_domains_exceptions(token, service):
    client = Client(token, service)
    with pytest.raises(MalformedDomain):
        client.get_domains(parent=1)
    with pytest.raises(MalformedDomain):
        client.get_domains(parent="U.S. states")


def test_delete_protected_domain_error(token, service):
    client = Client(token, service)
    client.bulk_create([{"name": "Kansas"}], domain="states")
    with pytest.raises(ProtectedDomainError):
        client.delete_domain("states")


def test_delete_domain(token, service):
    client = Client(token, service)
    # Client passed slug
    response = client.delete_domain("cities")
    assert response is True
    # Client passed instance
    domain = client.get_domain("counties")
    response = client.delete_domain(domain)
    assert response is True
    # Instance method
    domain = client.get_domain("townships")
    domain.delete()
    assert domain.deleted is True


def test_cleanup(token, service):
    client = Client(token, service, domain="states")
    client.delete_match({"name": "Kansas"})
    client.delete_domain("states")
