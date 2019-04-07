from crosswalk_client.exceptions import MalformedThreshold, MissingThreshold


def validate_required_threshold(function):
    """
    Validates a threshold.
    """

    def wrapper(*args, **kwargs):
        list_args = list(args)
        try:
            threshold = list_args[1]
        except IndexError:
            raise MissingThreshold("Must pass a threshold")
        if not isinstance(threshold, int):
            raise MalformedThreshold("Threshold must be an integer")
        if threshold < 0 or threshold > 100:
            raise MalformedThreshold("Threshold must be between 0 and 100")
        return function(*args, **kwargs)

    return wrapper
