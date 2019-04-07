from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.domain import DomainObject
from crosswalk_client.validators.domain import (
    validate_required_domain_string_arg
)


class GetDomain(object):
    @validate_required_domain_string_arg
    def get_domain(self, domain):
        response = requests.get(
            urljoin(self.service_address, f"domains/{domain}/"),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return DomainObject(response.json(), client=self)
