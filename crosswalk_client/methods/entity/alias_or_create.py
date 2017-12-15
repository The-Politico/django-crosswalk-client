from typing import Dict
from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import (validate_block_attrs,
                                         validate_create_attrs,
                                         validate_domain, validate_query,
                                         validate_threshold)
from crosswalk_client.exceptions import BadResponse, CreateEntityError
from crosswalk_client.methods.objectify import AttributeObject


class AliasOrCreate(object):
    @validate_query
    @validate_block_attrs
    @validate_create_attrs
    @validate_domain
    @validate_threshold
    def alias_or_create(
        self,
        query: Dict[str, str],
        block_attrs: dict = {},
        create_attrs: dict = {},
        domain: str = None,
        threshold: int = None
    ):
        if domain is None:
            domain = self.domain
        if threshold is None:
            threshold = self.threshold
        query_field = list(query.keys())[0]
        data = {
            "query_field": query_field,
            "query_value": query[query_field],
            "threshold": threshold,
            "block_attrs": block_attrs,
            "create_attrs": create_attrs,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/alias-or-create/'.format(domain),
            ),
            headers=self.headers,
            json=data
        )
        if response.status_code == 404:
            raise CreateEntityError(
                'Error creating entities: {}'.format(
                    response.content,
                )
            )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return AttributeObject(response.json())
