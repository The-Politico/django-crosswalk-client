from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse


class BulkCreate(object):
    """
    Bulk create entities.

    entites should be an array of attributes objects.

    Passing force_bulk True will use Django bulk_create, which is fast.
    Otherwise, we use Django get_or_create to avoid creating duplicates.
    """
    def bulk_create(
        self,
        domain,
        entities,
        force_bulk=False
    ):
        data = {
            "domain": domain,
            "entities": entities,
            "force_bulk": force_bulk
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'bulk-create/{}/'.format(domain),
            ),
            headers=self.headers,
            json=data
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code.'.format(
                  response.status_code
                ))
        return response
