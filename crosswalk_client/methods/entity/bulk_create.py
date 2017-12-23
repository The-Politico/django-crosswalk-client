from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_domain
from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse, CreateEntityError
from crosswalk_client.objects.entity import EntityObject


class BulkCreate(object):
    """
    Bulk create entities.

    Entites should be an array of attributes dicts.
    """
    @validate_domain
    def bulk_create(
        self,
        entities,
        domain=None,
    ):
        if domain is None:
            domain = self.domain
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/bulk-create/'.format(domain),
            ),
            headers=self.headers,
            data=encode(entities),
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
            EntityObject(entity, client=self)
            for entity in response.json()['entities']
        ]
