from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.methods.objectify import AttributeObject


class BestMatch(object):
    def best_match(
        self,
        query,
        match_attrs={},
        domain=None,
    ):
        if domain:
            self.domain = domain
        query_field = list(query.keys())[0]
        data = {
            **match_attrs,
            **{
                "query_field": query_field,
                "query_value": query[query_field]
            },
        }
        response = requests.get(
            urljoin(
                self.service_address,
                'best-match/{}/'.format(self.domain),
            ),
            headers=self.headers,
            params=data
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code. {}'.format(
                  response.status_code
                ))
        return AttributeObject(response.json())
