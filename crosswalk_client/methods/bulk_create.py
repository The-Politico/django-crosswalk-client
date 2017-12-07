from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse


class BulkCreate(object):
    """
    Bulk create entities.

    entites should be an array of attributes objects.
    """
    def bulk_create(
        self,
        entities,
        domain=None,
    ):
        if domain:
            self.domain = domain
        response = requests.post(
            urljoin(
                self.service_address,
                'bulk-create/{}/'.format(self.domain),
            ),
            headers=self.headers,
            json=entities
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code.'.format(
                  response.status_code
                ))
        return response.status_code == requests.codes.ok
