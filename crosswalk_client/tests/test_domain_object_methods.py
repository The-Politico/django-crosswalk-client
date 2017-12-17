from crosswalk_client import Client


def test_setup(token, service):
    client = Client(token, service)
    client.create_domain('presidents')
    client.create_domain('politicians')


def test_domain_update(token, service):
    client = Client(token, service)
    domain = client.get_domain('presidents')
    domain.update({"name": "Presidents"})
    assert domain.name == "Presidents"


def test_domain_set_parent(token, service):
    client = Client(token, service)
    domain = client.get_domain('politicians')
    domain.set_parent(client.get_domain('presidents'))
    assert domain.parent == "presidents"


def test_domain_remove_parent(token, service):
    client = Client(token, service)
    domain = client.get_domain('politicians')
    domain.remove_parent()
    assert domain.parent is None


def test_domain_delete(token, service):
    client = Client(token, service)
    domain = client.get_domain('politicians')
    domain.delete()
    assert domain.deleted is True

    domain = client.get_domain('presidents')
    domain.delete()
    assert domain.deleted is True
