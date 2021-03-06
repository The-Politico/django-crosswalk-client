from urllib.parse import urljoin

import requests

from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject
from crosswalk_client.validators.entity import (
    validate_required_update_attrs_arg,
    validate_required_uuid_arg,
)


class UpdateById(object):
    """
    Update an entity.
    """

    @validate_required_uuid_arg
    @validate_required_update_attrs_arg
    def update_by_id(self, uuid, update_attrs):
        response = requests.patch(
            urljoin(self.service_address, "entities/{}/".format(uuid)),
            headers=self.headers,
            data=encode({"attributes": update_attrs}),
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return EntityObject({"entity": response.json()}, client=self)
