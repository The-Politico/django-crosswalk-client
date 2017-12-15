from typing import Dict
from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import (validate_block_attrs,
                                         validate_create_attrs,
                                         validate_domain, validate_query,
                                         validate_threshold)
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.methods.objectify import AttributeObject


class BestMatchOrCreate(object):
    @validate_query
    @validate_block_attrs
    @validate_create_attrs
    @validate_domain
    @validate_threshold
    def best_match_or_create(
        self,
        query: Dict[str, str],
        block_attrs: dict = {},
        create_attrs: dict = {},
        domain: str = None,
        threshold: int = None,
        scorer: str = None,
    ):
        if domain is None:
            domain = self.domain
        if threshold is None:
            threshold = self.threshold
        if scorer is None:
            scorer = self.scorer
        query_field = list(query.keys())[0]
        data = {
            "query_field": query_field,
            "query_value": query[query_field],
            "threshold": threshold,
            "block_attrs": block_attrs,
            "create_attrs": create_attrs,
            "scorer": scorer,
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
        return AttributeObject(response.json())
