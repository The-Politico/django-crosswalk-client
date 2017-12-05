from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse


class CreateDomain(object):
    """ Create a domain. """
    def create_domain(
        self,
        domain,
        parent=None,
    ):
        if parent:
            data = {
                "name": domain,
                "parent": parent,
            }
        else:
            data = {"name": domain}
        response = requests.post(
            urljoin(self.service_address, 'domains/'),
            headers=self.headers,
            json=data
        )
        if response.status_code != 201:
            raise BadResponse(
                'The service responded with a {} status code.'.format(
                  response.status_code
                ))
        return response.json()
