from urllib.parse import urljoin

import requests
from slugify import slugify

from crosswalk_client.exceptions import (BadResponse, MalformedDomain,
                                         ProtectedDomainError)
from crosswalk_client.objects.domain import DomainObject


class DeleteDomain(object):
    """
    Delete a domain.
    """

    def delete_domain(self, domain):
        if isinstance(domain, DomainObject):
            slug = domain.slug
        elif isinstance(domain, str):
            slug = slugify(domain)
        else:
            raise MalformedDomain(
                "You didn't provide a domain instance or slug."
            )
        response = requests.delete(
            urljoin(self.service_address, f"domains/{slug}/"),
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
