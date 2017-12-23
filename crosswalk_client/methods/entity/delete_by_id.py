from urllib.parse import urljoin

import requests

from crosswalk_client.decorators import validate_uuid
from crosswalk_client.exceptions import BadResponse


class DeleteById(object):
    """
    Delete an entity.
    """
    @validate_uuid
    def delete_by_id(
        self,
        uuid,
    ):
        response = requests.delete(
            urljoin(
                self.service_address,
                'entities/{}/'.format(uuid),
            ),
            headers=self.headers,
        )
        if response.status_code != 204:
            raise BadResponse(
                'The service responded with a {}: {}'.format(
                  response.status_code,
                  response.content,
                ))
        return True
