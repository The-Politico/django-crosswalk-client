from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.methods.objectify import AttributeObject


class UpdateDomain(object):
    """
    Update a domain.
    """
    def update_domain(
        self,
        slug: str,
        update: dict,
    ):
        response = requests.patch(
            urljoin(
                self.service_address,
                'domains/{}/'.format(slug),
            ),
            headers=self.headers,
            json=update
        )
        if response.status_code != 200:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return AttributeObject(response.json())
