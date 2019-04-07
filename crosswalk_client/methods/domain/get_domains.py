from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.domain import DomainObject
from crosswalk_client.validators.domain import validate_parent_domain_kwarg


class GetDomains(object):
    @validate_parent_domain_kwarg
    def get_domains(self, parent=None):
        params = {}
        if parent:
            params["parent"] = parent
        response = requests.get(
            urljoin(self.service_address, "domains/"),
            headers=self.headers,
            params=params,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        domains = response.json()
        return [DomainObject(domain, client=self) for domain in domains]
