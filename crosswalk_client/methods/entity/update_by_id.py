from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_update_attrs
from crosswalk_client.exceptions import BadRequest, BadResponse
from crosswalk_client.methods.objectify import AttributeObject


class UpdateById(object):
    """
    Delete an entity.
    """
    @validate_update_attrs
    def update_by_id(
        self,
        uuid: str,
        update_attrs: dict,
    ):
        if not isinstance(update_attrs, dict):
            raise BadRequest(
                'update_attrs must be a dictionary of attributes.'
            )
        response = requests.patch(
            urljoin(
                self.service_address,
                'entities/{}/'.format(uuid),
            ),
            headers=self.headers,
            json={"attributes": update_attrs}
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return AttributeObject({"entity": response.json()})
