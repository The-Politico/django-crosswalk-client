from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import (BadResponse,
                                         UnspecificDeleteRequestError)


class DeleteMatch(object):
    def delete_match(
        self,
        block_attrs,
        domain=None,
    ):
        if domain:
            self.domain = domain
        data = block_attrs
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/delete-match/'.format(self.domain),
            ),
            headers=self.headers,
            json=data
        )
        if response.status_code == 403:
            raise UnspecificDeleteRequestError(
                "Delete request matched more than one record."
            )
        if response.status_code != 204:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return response.status_code == 204
