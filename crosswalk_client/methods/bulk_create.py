from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse, CreateEntityError
from crosswalk_client.methods.objectify import AttributeObject


class BulkCreate(object):
    """
    Bulk create entities.

    Entites should be an array of attributes dicts.
    """
    def bulk_create(
        self,
        entities,
        domain=None,
    ):
        if domain:
            self.domain = domain
        response = requests.post(
            urljoin(
                self.service_address,
                'bulk-create/{}/'.format(self.domain),
            ),
            headers=self.headers,
            json=entities
        )
        if response.status_code == 400:
            raise CreateEntityError(
                'Error creating entities: {}'.format(
                    response.json().get('message', 'No further detail.')
                )
            )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.json().get('message', 'No further detail.')
                ))
        return [
            AttributeObject(entity)
            for entity in response.json()['entities']
        ]
