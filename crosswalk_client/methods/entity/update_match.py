from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import (validate_block_attrs, validate_domain,
                                         validate_update_attrs)
from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import (BadResponse,
                                         UnspecificUpdateRequestError,
                                         UpdateEntityError)
from crosswalk_client.objects.entity import EntityObject


class UpdateMatch(object):
    """
    Update a match.

    Entites should be an array of attributes dicts.
    """
    @validate_block_attrs
    @validate_update_attrs
    @validate_domain
    def update_match(
        self,
        block_attrs,
        update_attrs,
        domain=None,
    ):
        if domain is None:
            domain = self.domain
        data = {
            "block_attrs": block_attrs,
            "update_attrs": update_attrs,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/update-match/'.format(domain),
            ),
            headers=self.headers,
            data=encode(data),
        )
        if response.status_code == 403:
            raise UnspecificUpdateRequestError(response.content)
        if response.status_code == 400:
            raise UpdateEntityError(response.content)
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return EntityObject(response.json(), client=self)
