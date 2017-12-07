from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse


class DeleteMatch(object):
    def delete_match(
        self,
        match_attrs,
        domain=None,
    ):
        if domain:
            self.domain = domain
        data = match_attrs
        response = requests.post(
            urljoin(
                self.service_address,
                'delete-match/{}/'.format(self.domain),
            ),
            headers=self.headers,
            json=data
        )
        if response.status_code != 204:
            raise BadResponse(
                'The service responded with a {} status code. {}'.format(
                  response.status_code
                ))
        return response.status_code == 204
