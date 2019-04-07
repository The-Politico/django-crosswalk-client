from crosswalk_client.exceptions import MalformedDomain, MissingDomain


def validate_required_domain_string_arg(function):
    """
    Validates a domain string name is passed.
    """

    def wrapper(*args, **kwargs):
        list_args = list(args)
        try:
            domain = list_args[1]
        except IndexError:
            raise MissingDomain("Must pass a domain")
        if not isinstance(domain, str):
            raise MalformedDomain("Domain must be a string or domain instance")
        return function(*args, **kwargs)

    return wrapper
