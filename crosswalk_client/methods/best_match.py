from urllib.parse import urljoin

import requests

from crosswalk_client.exceptions import BadResponse


class BestMatch(object):
    def best_match(
        self,
        domain,
        query,
        match_attrs={},
        create_attrs={},
        create_threshold=None,
    ):
        if create_threshold:
            self.create_threshold = create_threshold
        query_field = list(query.keys())[0]
        data = {
            "query": {
                "field": query_field,
                "value": query[query_field]
            },
            "match_attrs": match_attrs,
            "create_attrs": {
                **query,
                **match_attrs,
                **create_attrs,
            },
            "create_threshold": create_threshold or self.create_threshold
        }
        response = requests.post(
            urljoin(
                self.service_address,
                'best-match/{}/'.format(domain),
            ),
            headers=self.headers,
            json=data
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                'The service responded with a {} status code.'.format(
                  response.status_code
                ))
        return response.json()
