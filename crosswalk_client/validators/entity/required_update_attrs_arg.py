from crosswalk_client.exceptions import MalformedUpdateAttributes


def validate_required_update_attrs_arg(function):
    def wrapper(*args, **kwargs):
        update_attrs = args[2]
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
