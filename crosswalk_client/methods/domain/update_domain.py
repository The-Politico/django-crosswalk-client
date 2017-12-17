from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.domain import DomainObject


class UpdateDomain(object):
    """
    Update a domain.
    """
    def update_domain(
        self,
        slug,
        update_attrs,
    ):
        response = requests.patch(
            urljoin(
                self.service_address,
                'domains/{}/'.format(slug),
            ),
            headers=self.headers,
            json=update_attrs
        )
        if response.status_code != 200:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return DomainObject(response.json(), client=self)
