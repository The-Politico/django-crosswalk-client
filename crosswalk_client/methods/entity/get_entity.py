from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_uuid
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject


class GetEntity(object):
    @validate_uuid
    def get_entity(
        self,
        uuid,
    ):
        response = requests.get(
            urljoin(
                self.service_address,
                'entities/{}/'.format(uuid),
            ),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        entity = response.json()
        return EntityObject({"entity": entity}, client=self)
