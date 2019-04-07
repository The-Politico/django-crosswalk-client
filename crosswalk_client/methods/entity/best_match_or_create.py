from urllib.parse import urljoin

import requests

from crosswalk_client.encoder import encode
from crosswalk_client.exceptions import BadResponse
from crosswalk_client.objects.entity import EntityObject
from crosswalk_client.validators.entity import (
    validate_block_attrs_kwarg,
    validate_create_attrs_kwarg,
    validate_domain_kwarg,
    validate_required_query_arg,
    validate_threshold_kwarg,
)


class BestMatchOrCreate(object):
    @validate_required_query_arg
    @validate_block_attrs_kwarg
    @validate_create_attrs_kwarg
    @validate_domain_kwarg
    @validate_threshold_kwarg
    def best_match_or_create(
        self,
        query,
        block_attrs={},
        create_attrs={},
        domain=None,
        threshold=None,
        scorer=None,
        return_canonical=True,
    ):
        if domain is None:
            domain = self.domain
        if threshold is None:
            threshold = self.threshold
        if scorer is None:
            scorer = self.scorer
        query_field = list(query.keys())[0]
        data = {
            "query_field": query_field,
            "query_value": query[query_field],
            "threshold": threshold,
            "block_attrs": block_attrs,
            "create_attrs": create_attrs,
            "scorer": scorer,
            "return_canonical": return_canonical,
        }
        response = requests.post(
            urljoin(
                self.service_address,
                "domains/{}/entities/best-match-or-create/".format(domain),
            ),
            headers=self.headers,
            data=encode(data),
        )
        if response.status_code != requests.codes.ok:
            raise BadResponse(
                "The service responded with a {}: {}".format(
                    response.status_code, response.content
                )
            )
        return EntityObject(response.json(), client=self)
