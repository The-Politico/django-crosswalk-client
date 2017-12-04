import requests
import os
from .exceptions import ConfigError


class Client(object):
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

    def client_check(self):
        r = requests.get(
            os.path.join(self.service_address, 'client-check/'),
            headers=self.headers,
        )
        if r.status_code != requests.codes.ok:
            raise ConfigError(
                'Client configuration error. Check that the token and service '
                'address are correctly configured.'
            )
        return r.status_code

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
            os.path.join(
                self.service_address,
                'best-match',
                domain,
            ) + os.path.sep,
            headers=self.headers,
            json=data
        )
        return r.json()

    def create_domain(
        self,
        domain,
    ):
        data = {
            "name": domain
        }
        r = requests.post(
            os.path.join(
                self.service_address,
                'domains',
            ) + os.path.sep,
            headers=self.headers,
            json=data
        )
        return r.json()

    def delete_domain(
        self,
        domain,
    ):
        response = requests.delete(
            os.path.join(
                self.service_address,
                'domains',
                domain
            ) + os.path.sep,
            headers=self.headers,
        )
        return response

    def bulk_create(
        self,
        domain,
        entities,
        force_bulk=False
    ):
        data = {
            "domain": domain,
            "entities": entities,
            "force_bulk": force_bulk
        }
        r = requests.post(
            os.path.join(
                self.service_address,
                'bulk-create',
                domain,
            ) + os.path.sep,
            headers=self.headers,
            json=data
        )
        return r
