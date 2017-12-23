from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_block_attrs, validate_domain
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject


class GetEntities(object):
    @validate_block_attrs
    @validate_domain
    def get_entities(
        self,
        block_attrs={},
        domain=None,
    ):
        if domain is None:
            domain = self.domain
        response = requests.get(
            urljoin(
                self.service_address,
                'domains/{}/entities/'.format(domain),
            ),
            headers=self.headers,
            params=block_attrs
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        entities = response.json()
        return [
            EntityObject({"entity": entity}, client=self)
            for entity in entities
        ]
