import pytest
from crosswalk_client import Client
from crosswalk_client.exceptions import (
    ConfigError,
    MalformedDomain,
    MalformedScorer,
    MalformedThreshold,
    MissingDomain,
    MissingScorer,
    MissingThreshold,
)


def test_misconfigured_config(token, service):
    with pytest.raises(ConfigError):
        Client("NOTAVALIDTOKEN", service)


def test_properly_configured_config(token, service):
    client = Client(token, service)
    response = client.client_check()
    assert response is True


def test_set_threshold(token, service):
    client = Client(token, service)
    client.set_threshold(99)
    assert client.threshold == 99


def test_set_threshold_exceptions(token, service):
    client = Client(token, service)
    with pytest.raises(MissingThreshold):
        client.set_threshold()
    with pytest.raises(MalformedThreshold):
        client.set_threshold(200)
    with pytest.raises(MalformedThreshold):
        client.set_threshold("asd")


def test_set_domain(token, service):
    client = Client(token, service)
    client.set_domain("sharks")
    assert client.domain == "sharks"

    domain = client.create_domain("whales")
    client.set_domain(domain)
    assert client.domain == "whales"

    domain.delete()


def test_set_domain_exceptions(token, service):
    client = Client(token, service)
    with pytest.raises(MissingDomain):
        client.set_domain()
    with pytest.raises(MalformedDomain):
        client.set_domain("U.S. states")


def test_set_scorer(token, service):
    client = Client(token, service)
    client.set_scorer("fuzzywuzzy.partial_ratio_process")
    assert client.scorer == "fuzzywuzzy.partial_ratio_process"


def test_set_scorer_exceptions(token, service):
    client = Client(token, service)
    with pytest.raises(MissingScorer):
        client.set_scorer()
    with pytest.raises(MalformedScorer):
        client.set_scorer("random.scorer")
