from uuid import UUID

from crosswalk_client.exceptions import MalformedUUID


def validate_required_uuid_arg(function):
    def wrapper(*args, **kwargs):
        uuid = args[1]
        if not isinstance(uuid, UUID):
            raise MalformedUUID("Invalid UUID")
        return function(*args, **kwargs)

    return wrapper
