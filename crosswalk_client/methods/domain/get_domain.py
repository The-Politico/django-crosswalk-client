from urllib.parse import urljoin

import requests
from slugify import slugify

from crosswalk_client.exceptions import BadResponse, MalformedDomain
from crosswalk_client.objects.domain import DomainObject


class GetDomain(object):
    def get_domain(self, domain):
        if isinstance(domain, str):
            slug = slugify(domain)
        else:
            raise MalformedDomain("You didn't provide a domain slug.")
        response = requests.get(
            urljoin(self.service_address, f"domains/{slug}/"),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return DomainObject(response.json(), client=self)
