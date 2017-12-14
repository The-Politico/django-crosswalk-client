from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import ConfigError


class ClientCheck(object):
    """Check if client was configured correctly and is authorized."""
    def client_check(self):
        response = requests.get(
            urljoin(self.service_address, 'client-check/'),
            headers=self.headers,
        )
        if response.status_code != requests.codes.ok:
            raise ConfigError(
                'Client configuration error. Check that the token and service '
                'address are correctly configured.'
            )
        return response.status_code == requests.codes.ok
