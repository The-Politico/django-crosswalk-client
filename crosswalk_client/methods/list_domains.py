from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse


class ListDomains(object):
    def list_domains(self):
        response = requests.get(
            urljoin(
                self.service_address,
                'domains/',
            ),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code.'.format(
                  response.status_code
                ))
        return response.json()
