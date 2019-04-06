from urllib.parse import urljoin

import requests
from slugify import slugify

from crosswalk_client.exceptions import BadResponse, MalformedDomain
from crosswalk_client.objects.domain import DomainObject


class GetDomains(object):
    def get_domains(self, parent=None):
        params = {}
        if parent:
            if isinstance(parent, DomainObject):
                params["parent"] = parent.slug
            elif isinstance(parent, str):
                params["parent"] = slugify(parent)
            else:
                raise MalformedDomain(
                    "You didn't pass parent as a Domain instance or slug."
                )
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
