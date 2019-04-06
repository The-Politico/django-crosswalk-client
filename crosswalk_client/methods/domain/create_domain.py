from urllib.parse import urljoin

import requests
from slugify import slugify

from crosswalk_client.exceptions import BadResponse, MalformedDomain
from crosswalk_client.objects.domain import DomainObject


class CreateDomain(object):
    """ Create a domain. """

    def create_domain(self, domain, parent=None):
        if not isinstance(domain, str):
            raise MalformedDomain(
                "You didn't pass a string for your domain name."
            )
        if parent:
            if isinstance(parent, DomainObject):
                data = {"name": domain, "parent": parent.slug}
            elif isinstance(parent, str):
                data = {"name": domain, "parent": slugify(parent)}
            else:
                raise MalformedDomain(
                    "Parent should be a Domain instance or slug."
                )
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
