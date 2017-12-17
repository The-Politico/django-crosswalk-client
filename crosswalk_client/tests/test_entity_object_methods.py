from crosswalk_client import Client


def test_setup(token, service):
    client = Client(token, service)
    client.create_domain('presidents')
    client.create_domain('politicians')
    client.bulk_create([{
        "name": "George W. Bush"
    }], domain="politicians")
    client.bulk_create([{
        "name": "George W. Bush"
    }], domain="presidents")
    client.bulk_create([{
        "name": "George Bush, Jr."
    }], domain="presidents")


def test_entity_update(token, service):
    client = Client(token, service, domain="presidents")
    entity = client.best_match({"name": "George W. Bush"})
    entity.update({"number": 43})
    assert entity.number == 43


def test_entity_set_alias_for(token, service):
    client = Client(token, service, domain="presidents")
    entity = client.best_match({"name": "George W. Bush"})
    alias = client.best_match({"name": "George Bush, Jr."})
    alias.set_alias_for(entity)
    assert alias.alias_for == entity.uuid


def test_entity_remove_alias_for(token, service):
    client = Client(token, service, domain="presidents")
    entity = client.best_match(
        {"name": "George Bush, Jr."}, return_canonical=False)
    assert entity.name == "George Bush, Jr."
    entity.remove_alias_for()
    assert entity.alias_for is None


def test_entity_set_superseded_by(token, service):
    client = Client(token, service)
    entity = client.best_match({"name": "George W. Bush"}, domain="presidents")
    superseded = client.best_match(
        {"name": "George W. Bush"}, domain="politicians")
    superseded.set_superseded_by(entity)
    assert superseded.superseded_by == entity.uuid


def test_entity_remove_superseded_by(token, service):
    client = Client(token, service, domain="politicians")
    entity = client.best_match({"name": "George W. Bush"})
    entity.remove_superseded_by()
    assert entity.superseded_by is None


def test_entity_delete(token, service):
    client = Client(token, service, domain="presidents")
    entity = client.best_match({"name": "George W. Bush"})
    entity.delete()
    assert entity.deleted is True

    entity = client.best_match(
        {"name": "George Bush, Jr."}, return_canonical=False)
    entity.delete()
    assert entity.deleted is True

    entity = client.best_match(
        {"name": "George W. Bush"}, domain="politicians")
    entity.delete()
    assert entity.deleted is True


def test_cleanup(token, service):
    client = Client(token, service)
    client.delete_domain('presidents')
    client.delete_domain('politicians')
