from slugify import slugify

from crosswalk_client.exceptions import MalformedDomain
from crosswalk_client.objects.domain import DomainObject


class SetDomain(object):
    def set_domain(self, domain):
        if isinstance(domain, DomainObject):
            self.domain = domain.slug
        elif isinstance(domain, str):
            self.domain = slugify(domain)
        else:
            raise MalformedDomain("Domain should be a domain instance or slug")
