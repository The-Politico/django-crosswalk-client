from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.domain import DomainObject


class GetDomains(object):
    def get_domains(self):
        response = requests.get(
            urljoin(
                self.service_address,
                'domains/',
            ),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        domains = response.json()
        return [DomainObject(domain, client=self) for domain in domains]
