from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_block_attrs, validate_domain
from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import (BadRequest, BadResponse,
                                         UnspecificDeleteRequestError)


class DeleteMatch(object):
    @validate_block_attrs
    @validate_domain
    def delete_match(
        self,
        block_attrs,
        domain=None,
    ):
        if not isinstance(block_attrs, dict):
            raise BadRequest(
                'block_attrs must be a dictionary of attributes.'
            )
        if domain is None:
            domain = self.domain
        data = block_attrs
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/delete-match/'.format(domain),
            ),
            headers=self.headers,
            data=encode(data)
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
