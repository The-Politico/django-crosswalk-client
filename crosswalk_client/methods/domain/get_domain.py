from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.domain import DomainObject


class GetDomain(object):
    def get_domain(self, slug):
        response = requests.get(
            urljoin(
                self.service_address,
                'domains/{}/'.format(slug),
            ),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return DomainObject(response.json(), client=self)
