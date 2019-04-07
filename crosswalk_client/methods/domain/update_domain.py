from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.domain import DomainObject
from crosswalk_client.validators.domain import validate_required_domain_arg


class UpdateDomain(object):
    @validate_required_domain_arg
    def update_domain(self, domain, update_attrs):
        response = requests.patch(
            urljoin(self.service_address, f"domains/{domain}/"),
            headers=self.headers,
            json=update_attrs,
        )
        if response.status_code != 200:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return DomainObject(response.json(), client=self)
