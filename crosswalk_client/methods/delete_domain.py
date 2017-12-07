from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse, ProtectedDomainError


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
        if response.status_code == 500:
            raise ProtectedDomainError(
                'Could not delete domain. It may have protected entites.'
            )
        if response.status_code != 204:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.json().get('message', 'No further detail.')
                ))
        return response.status_code == 204
