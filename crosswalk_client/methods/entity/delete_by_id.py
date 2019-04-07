from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse
from crosswalk_client.validators.entity import validate_required_uuid_arg


class DeleteById(object):
    @validate_required_uuid_arg
    def delete_by_id(self, uuid):
        response = requests.delete(
            urljoin(self.service_address, "entities/{}/".format(uuid)),
            headers=self.headers,
        )
        if response.status_code != 204:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return True
