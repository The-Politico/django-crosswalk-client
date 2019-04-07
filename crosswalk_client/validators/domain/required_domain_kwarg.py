from slugify import slugify

from crosswalk_client.exceptions import MalformedDomain, MissingDomain
from crosswalk_client.objects.domain import DomainObject


def validate_required_domain_kwarg(function):
    """
    Validates a domain is passed. Converts DomainObject instances to slug.
    """

    def wrapper(*args, **kwargs):
        domain = kwargs.get("domain", None)
        if domain is None:
            raise MissingDomain("Must pass a domain")
        if isinstance(domain, DomainObject):
            kwargs["domain"] = domain.slug
            return function(*args, **kwargs)
        if not isinstance(domain, str):
            raise MalformedDomain("Domain must be a string or domain instance")
        if slugify(domain) != domain:
            raise MalformedDomain("Domain string should be a slug")
        return function(*args, **kwargs)

    return wrapper
