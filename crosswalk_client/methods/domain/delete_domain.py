from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse, ProtectedDomainError
from crosswalk_client.validators.domain import validate_required_domain_arg


class DeleteDomain(object):
    @validate_required_domain_arg
    def delete_domain(self, domain):
        response = requests.delete(
            urljoin(self.service_address, f"domains/{domain}/"),
            headers=self.headers,
        )
        if response.status_code == 500:
            raise ProtectedDomainError(
                "Could not delete domain. It may have protected entites."
            )
        if response.status_code != 204:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return True
