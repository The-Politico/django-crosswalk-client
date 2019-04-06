from uuid import UUID

from slugify import slugify

from crosswalk_client.exceptions import (MalformedBlockAttributes,
                                         MalformedCreateAttributes,
                                         MalformedDomain, MalformedQuery,
                                         MalformedThreshold,
                                         MalformedUpdateAttributes,
                                         MalformedUUID, MissingDomain)
from crosswalk_client.objects.domain import DomainObject


def validate_query(function):
    def wrapper(*args, **kwargs):
        query = args[1]
        if not isinstance(query, dict):
            raise MalformedQuery("Query should be a dictionary")
        if len(query.keys()) > 1:
            raise MalformedQuery(
                "Query should only include one key value pair"
            )
        if not isinstance(list(query.values())[0], str) or not isinstance(
            list(query.keys())[0], str
        ):
            raise MalformedQuery("Query key and value should be strings")
        return function(*args, **kwargs)

    return wrapper


def validate_block_attrs(function):
    def wrapper(*args, **kwargs):
        block_attrs = kwargs.get("block_attrs", {}).copy()
        if not isinstance(block_attrs, dict):
            raise MalformedBlockAttributes(
                "Block attributes must be a dictionary"
            )
        for key in block_attrs:
            if isinstance(block_attrs[key], dict):
                raise MalformedBlockAttributes(
                    "Nested attributes are not allowed in block attributes"
                )
        return function(*args, **kwargs)

    return wrapper


def validate_create_attrs(function):
    def wrapper(*args, **kwargs):
        create_attrs = kwargs.get("create_attrs", {}).copy()
        if not isinstance(create_attrs, dict):
            raise MalformedCreateAttributes(
                "Create attributes must be a dictionary"
            )
        for key in create_attrs:
            if isinstance(create_attrs[key], dict):
                raise MalformedCreateAttributes(
                    "Nested attributes are not allowed in create attributes"
                )
        return function(*args, **kwargs)

    return wrapper


def validate_update_attrs(function):
    def wrapper(*args, **kwargs):
        update_attrs = kwargs.get("update_attrs", {}).copy()
        if not isinstance(update_attrs, dict):
            raise MalformedUpdateAttributes(
                "Update attributes must be a dictionary"
            )
        for key in update_attrs:
            if isinstance(update_attrs[key], dict):
                raise MalformedUpdateAttributes(
                    "Nested attributes are not allowed in update attributes"
                )
        return function(*args, **kwargs)

    return wrapper


def validate_domain(function):
    def wrapper(*args, **kwargs):
        domain = kwargs.get("domain", args[0].domain)
        if domain is None:
            raise MissingDomain("Must set a domain")
        if isinstance(domain, DomainObject):
            if "domain" in kwargs:
                kwargs["domain"] = domain.slug
            else:
                args[0].domain = domain.slug
            return function(*args, **kwargs)
        if not isinstance(domain, str):
            raise MalformedDomain(
                "Domain must be a string or domain instance"
            )
        if slugify(domain) != domain:
            raise MalformedDomain("Domain string should be a slug")
        return function(*args, **kwargs)

    return wrapper


def validate_threshold(function):
    def wrapper(*args, **kwargs):
        threshold = kwargs.get("threshold", args[0].threshold)
        if not isinstance(threshold, int):
            raise MalformedThreshold("Threshold should be an integer")
        if threshold < 0 or threshold > 100:
            raise MalformedThreshold("Threshold should be between 0 and 100")
        return function(*args, **kwargs)

    return wrapper


def validate_uuid(function):
    def wrapper(*args, **kwargs):
        uuid = args[1]
        if not isinstance(uuid, UUID):
            raise MalformedUUID("Invalid UUID")
        return function(*args, **kwargs)

    return wrapper


def validate_target_uuid(function):
    """
    Target UUIDs are used to set foreign keys and should be either a valid UUID
    or None to unset the foreign key.
    """

    def wrapper(*args, **kwargs):
        uuid = args[2]
        if uuid is not None and not isinstance(uuid, UUID):
            raise MalformedUUID("Invalid UUID for target")
        return function(*args, **kwargs)

    return wrapper
