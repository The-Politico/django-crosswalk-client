from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import (validate_block_attrs, validate_domain,
                                         validate_query)
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject


class BestMatch(object):
    @validate_query
    @validate_block_attrs
    @validate_domain
    def best_match(
        self,
        query,
        block_attrs={},
        domain=None,
        scorer=None,
        return_canonical=True,
    ):
        if domain is None:
            domain = self.domain
        if scorer is None:
            scorer = self.scorer
        query_field = list(query.keys())[0]
        data = {
            "block_attrs": block_attrs,
            "query_field": query_field,
            "query_value": query[query_field],
            "return_canonical": return_canonical,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/best-match/'.format(domain),
            ),
            headers=self.headers,
            json=data
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return EntityObject(response.json(), client=self)
