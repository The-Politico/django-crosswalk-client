from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse


class DeleteDomain(object):
    """
    Delete a domain.
    """
    def delete_domain(
        self,
        domain,
    ):
        response = requests.delete(
            urljoin(
                self.service_address,
                'domains/{}/'.format(domain),
            ),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code.'.format(
                  response.status_code
                ))
        return response
