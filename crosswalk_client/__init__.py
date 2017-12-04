import requests
from urllib.parse import urljoin
from .exceptions import ConfigError
from .methods import ClientMethods


class Client(ClientMethods):
    def __init__(
        self,
        token,
        service_address,
        create_threshold=0.5,
    ):
        self.token = token
        self.service_address = service_address
        self.headers = {
            'Authorization': 'TOKEN {}'.format(self.token)
        }
        self.create_threshold = create_threshold
        self.client_check()

    def best_match(
        self,
        domain,
        query,
        match_attrs={},
        create_attrs={},
        create_threshold=None,
    ):
        if create_threshold:
            self.create_threshold = create_threshold
        query_field = list(query.keys())[0]
        data = {
            "query": {
                "field": query_field,
                "value": query[query_field]
            },
            "match_attrs": match_attrs,
            "create_attrs": {
                **query,
                **match_attrs,
                **create_attrs,
            },
            "create_threshold": create_threshold or self.create_threshold
        }
        r = requests.post(
            urljoin(
                self.service_address,
                'best-match/{}/'.format(domain),
            ),
            headers=self.headers,
            json=data
        )
        return r.json()
