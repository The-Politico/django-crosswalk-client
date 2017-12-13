from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import (BadResponse,
                                         UnspecificUpdateRequestError,
                                         UpdateEntityError)
from crosswalk_client.methods.objectify import AttributeObject


class UpdateMatch(object):
    """
    Update a match.

    Entites should be an array of attributes dicts.
    """
    def update_match(
        self,
        block_attrs,
        update_attrs,
        domain=None,
    ):
        if domain:
            self.domain = domain
        data = {
            "block_attrs": block_attrs,
            "update_attrs": update_attrs,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'domains/{}/entities/update-match/'.format(self.domain),
            ),
            headers=self.headers,
            json=data
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
        return AttributeObject(response.json())
