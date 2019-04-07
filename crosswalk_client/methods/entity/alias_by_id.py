from urllib.parse import urljoin

import requests

from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject
from crosswalk_client.validators.entity import (
    validate_required_uuid_arg,
    validate_target_uuid_arg,
)


class AliasById(object):
    """
    Alias an entity.
    """

    @validate_required_uuid_arg
    @validate_target_uuid_arg
    def alias_by_id(self, alias_uuid, alias_for_uuid):
        response = requests.patch(
            urljoin(self.service_address, "entities/{}/".format(alias_uuid)),
            headers=self.headers,
            data=encode({"alias_for": alias_for_uuid}),
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return EntityObject({"entity": response.json()}, client=self)
