from slugify import slugify

from crosswalk_client.exceptions import MalformedDomain, MissingDomain
from crosswalk_client.objects.domain import DomainObject


def validate_domain_kwarg(function):
    def wrapper(*args, **kwargs):
        client = args[0]
        domain = kwargs.get("domain", client.domain)
        if domain is None:
            raise MissingDomain("Must set a domain")
        if isinstance(domain, DomainObject):
            if "domain" in kwargs:
                kwargs["domain"] = domain.slug
            args[0].domain = domain.slug
            return function(*args, **kwargs)
        if not isinstance(domain, str):
            raise MalformedDomain("Domain must be a string or domain instance")
        if slugify(domain) != domain:
            raise MalformedDomain("Domain string should be a slug")
        return function(*args, **kwargs)

    return wrapper
