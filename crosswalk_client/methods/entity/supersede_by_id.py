from urllib.parse import urljoin

import requests

from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject
from crosswalk_client.validators.entity import (
    validate_required_uuid_arg,
    validate_target_uuid_arg,
)


class SupersedeById(object):
    """
    Supersede an entity.
    """

    @validate_required_uuid_arg
    @validate_target_uuid_arg
    def supersede_by_id(self, uuid, superseded_by_uuid):
        response = requests.patch(
            urljoin(self.service_address, "entities/{}/".format(uuid)),
            headers=self.headers,
            data=encode({"superseded_by": superseded_by_uuid}),
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return EntityObject({"entity": response.json()}, client=self)
