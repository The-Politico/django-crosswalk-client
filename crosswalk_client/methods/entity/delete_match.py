from urllib.parse import urljoin

import requests

from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import (
    BadRequest,
    BadResponse,
    UnspecificQueryError,
)
from crosswalk_client.validators.entity import (
    validate_domain_kwarg,
    validate_required_block_attrs_arg,
)


class DeleteMatch(object):
    @validate_required_block_attrs_arg
    @validate_domain_kwarg
    def delete_match(self, block_attrs, domain=None):
        if not isinstance(block_attrs, dict):
            raise BadRequest("block_attrs must be a dictionary of attributes.")
        if domain is None:
            domain = self.domain
        data = block_attrs
        response = requests.post(
            urljoin(
                self.service_address,
                "domains/{}/entities/delete-match/".format(domain),
            ),
            headers=self.headers,
            data=encode(data),
        )
        if response.status_code == 403:
            raise UnspecificQueryError(
                "Query in request matched more than one entity."
            )
        if response.status_code != 204:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return response.status_code == 204
