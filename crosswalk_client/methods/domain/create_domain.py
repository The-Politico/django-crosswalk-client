from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.domain import DomainObject
from crosswalk_client.validators.domain import (
    validate_parent_domain_kwarg,
    validate_required_domain_string_arg,
)


class CreateDomain(object):
    """ Create a domain. """

    @validate_parent_domain_kwarg
    @validate_required_domain_string_arg
    def create_domain(self, domain, parent=None):
        if parent:
            data = {"name": domain, "parent": parent}
        else:
            data = {"name": domain}
        response = requests.post(
            urljoin(self.service_address, "domains/"),
            headers=self.headers,
            json=data,
        )
        if response.status_code != 201:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return DomainObject(response.json(), client=self)
