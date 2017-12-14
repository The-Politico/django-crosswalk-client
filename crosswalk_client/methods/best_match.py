from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.methods.objectify import AttributeObject


class BestMatch(object):
    def best_match(
        self,
        query,
        block_attrs={},
        domain=None,
        scorer=None,
    ):
        if domain:
            self.domain = domain
        if scorer:
            self.scorer = scorer
        query_field = list(query.keys())[0]
        data = {
            **block_attrs,
            **{
                "query_field": query_field,
                "query_value": query[query_field]
            },
        }
        response = requests.get(
            urljoin(
                self.service_address,
                'domains/{}/entities/best-match/'.format(self.domain),
            ),
            headers=self.headers,
            params=data
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return AttributeObject(response.json())
