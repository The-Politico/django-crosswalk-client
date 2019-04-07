from crosswalk_client.exceptions import MalformedCreateAttributes


def validate_create_attrs_kwarg(function):
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
