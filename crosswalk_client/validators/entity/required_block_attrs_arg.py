from crosswalk_client.exceptions import MalformedBlockAttributes


def validate_required_block_attrs_arg(function):
    def wrapper(*args, **kwargs):
        block_attrs = args[1]
        if not isinstance(block_attrs, dict):
            raise MalformedBlockAttributes(
                "Block attributes must be a dictionary"
            )
        for key in block_attrs:
            if isinstance(block_attrs[key], dict):
                raise MalformedBlockAttributes(
                    "Nested attributes are not allowed in block attributes"
                )
        return function(*args, **kwargs)

    return wrapper
