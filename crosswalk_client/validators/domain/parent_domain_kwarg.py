from slugify import slugify

from crosswalk_client.exceptions import MalformedDomain
from crosswalk_client.objects.domain import DomainObject


def validate_parent_domain_kwarg(function):
    """
    Validates a domain is passed. Converts DomainObject instances to slug.
    """

    def wrapper(*args, **kwargs):
        parent = kwargs.get("parent", None)
        if parent is None:
            return function(*args, **kwargs)
        if isinstance(parent, DomainObject):
            kwargs["parent"] = parent.slug
            return function(*args, **kwargs)
        if not isinstance(parent, str):
            raise MalformedDomain(
                "Parent domain must be a string or domain instance"
            )
        if slugify(parent) != parent:
            raise MalformedDomain("Parent domain string should be a slug")
        return function(*args, **kwargs)

    return wrapper
