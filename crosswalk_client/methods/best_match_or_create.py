from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.methods.objectify import AttributeObject


class BestMatchOrCreate(object):
    def best_match_or_create(
        self,
        query,
        match_attrs={},
        domain=None,
        create_threshold=None
    ):
        if domain:
            self.domain = domain
        if create_threshold:
            self.create_threshold = create_threshold
        query_field = list(query.keys())[0]
        data = {
            "query_field": query_field,
            "query_value": query[query_field],
            "create_threshold": self.create_threshold,
            "match_attrs": match_attrs,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'best-match/{}/'.format(self.domain),
            ),
            headers=self.headers,
            json=data
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code. {}'.format(
                  response.status_code
                ))
        return AttributeObject(response.json())
