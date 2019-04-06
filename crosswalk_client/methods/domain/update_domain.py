from urllib.parse import urljoin

import requests
from slugify import slugify

from crosswalk_client.exceptions import BadResponse, MalformedDomain
from crosswalk_client.objects.domain import DomainObject


class UpdateDomain(object):
    """
    Update a domain.
    """

    def update_domain(self, domain, update_attrs):
        if isinstance(domain, DomainObject):
            slug = domain.slug
        elif isinstance(domain, str):
            slug = slugify(domain)
        else:
            raise MalformedDomain(
                "You didn't provide a domain instance or slug."
            )
        response = requests.patch(
            urljoin(self.service_address, f"domains/{slug}/"),
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
