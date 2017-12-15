from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_domain
from crosswalk_client.exceptions import BadResponse, CreateEntityError
from crosswalk_client.methods.objectify import AttributeObject


class BulkCreate(object):
    """
    Bulk create entities.

    Entites should be an array of attributes dicts.
    """
    @validate_domain
    def bulk_create(
        self,
        entities: list,
        domain: str = None,
    ):
        if domain is None:
            domain = self.domain
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/bulk-create/'.format(domain),
            ),
            headers=self.headers,
            json=entities
        )
        if response.status_code == 400:
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
        return [
            AttributeObject(entity)
            for entity in response.json()['entities']
        ]
