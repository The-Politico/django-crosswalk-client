from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_target_uuid, validate_uuid
from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject


class SupersedeById(object):
    """
    Supersede an entity.
    """
    @validate_uuid
    @validate_target_uuid
    def supersede_by_id(
        self,
        uuid,
        superseded_by_uuid,
    ):
        response = requests.patch(
            urljoin(
                self.service_address,
                'entities/{}/'.format(uuid),
            ),
            headers=self.headers,
            data=encode({"superseded_by": superseded_by_uuid}),
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return EntityObject({"entity": response.json()}, client=self)
