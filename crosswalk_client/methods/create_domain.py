from urllib.parse import urljoin
from crosswalk_client.exceptions import BadResponse

import requests


class CreateDomain(object):
    """ Create a domain. """
    def create_domain(
        self,
        domain,
    ):
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/',
            ),
            headers=self.headers,
            json={"name": domain}
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code.'.format(
                  response.status_code
                ))
        return response.json()
