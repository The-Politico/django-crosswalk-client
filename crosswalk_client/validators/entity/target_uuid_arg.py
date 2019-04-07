from uuid import UUID

from crosswalk_client.exceptions import MalformedUUID


def validate_target_uuid_arg(function):
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
