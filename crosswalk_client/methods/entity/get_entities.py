from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.methods.objectify import AttributeObject


class GetEntities(object):
    def get_entities(self, domain: str = None):
        if domain is None:
            domain = self.domain
        response = requests.get(
            urljoin(
                self.service_address,
                'domains/{}/entities/'.format(domain),
            ),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        entities = response.json()
        return [AttributeObject({"entity": entity}) for entity in entities]
