from urllib.parse import urljoin

import requests

from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import (
    BadResponse,
    UnspecificQueryError,
    EntityNotFoundError,
)
from crosswalk_client.objects.entity import EntityObject
from crosswalk_client.validators.entity import (
    validate_block_attrs_kwarg,
    validate_domain_kwarg,
    validate_required_query_arg,
)


class Match(object):
    @validate_required_query_arg
    @validate_block_attrs_kwarg
    @validate_domain_kwarg
    def match(
        self,
        query,
        block_attrs={},
        create_attrs={},
        domain=None,
        return_canonical=True,
    ):
        if domain is None:
            domain = self.domain
        query_field = list(query.keys())[0]
        data = {
            "query_field": query_field,
            "query_value": query[query_field],
            "block_attrs": block_attrs,
            "return_canonical": return_canonical,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                "domains/{}/entities/match/".format(domain),
            ),
            headers=self.headers,
            data=encode(data),
        )
        if response.status_code == 403:
            raise UnspecificQueryError(
                "Query in request matched more than one entity."
            )
        if response.status_code == 404:
            raise EntityNotFoundError("No entity found for the given query")
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return EntityObject(response.json(), client=self)
