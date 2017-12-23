from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_target_uuid, validate_uuid
from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject


class AliasById(object):
    """
    Alias an entity.
    """
    @validate_uuid
    @validate_target_uuid
    def alias_by_id(
        self,
        alias_uuid,
        alias_for_uuid,
    ):
        response = requests.patch(
            urljoin(
                self.service_address,
                'entities/{}/'.format(alias_uuid),
            ),
            headers=self.headers,
            data=encode({"alias_for": alias_for_uuid})
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return EntityObject({"entity": response.json()}, client=self)
