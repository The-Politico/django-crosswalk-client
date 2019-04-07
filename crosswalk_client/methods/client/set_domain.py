from crosswalk_client.validators.domain import validate_required_domain_arg


class SetDomain(object):
    @validate_required_domain_arg
    def set_domain(self, domain):
        self.domain = domain
