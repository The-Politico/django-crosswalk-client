from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse, CreateEntityError
from crosswalk_client.methods.objectify import AttributeObject


class CreateMatchedAlias(object):
    def create_matched_alias(
        self,
        query,
        block_attrs={},
        create_attrs={},
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
            "block_attrs": block_attrs,
            "create_attrs": create_attrs,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/create-matched-alias/'.format(
                    self.domain),
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
