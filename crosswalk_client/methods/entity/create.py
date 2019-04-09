from urllib.parse import urljoin

import requests

from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse, CreateEntityError
from crosswalk_client.objects.entity import EntityObject
from crosswalk_client.validators.entity import validate_domain_kwarg


class Create(object):
    """
    Create a single entity. (Just a shortcut to bulk create...)

    Entity should be a dict of attributes.
    """

    @validate_domain_kwarg
    def create(self, entity, domain=None):
        if domain is None:
            domain = self.domain
        response = requests.post(
            urljoin(
                self.service_address,
                "domains/{}/entities/bulk-create/".format(domain),
            ),
            headers=self.headers,
            data=encode([entity]),
        )
        if response.status_code == 400:
            raise CreateEntityError(
                "Error creating entity: {}".format(response.content)
            )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return [
            EntityObject(entity, client=self)
            for entity in response.json()["entities"]
        ][0]
