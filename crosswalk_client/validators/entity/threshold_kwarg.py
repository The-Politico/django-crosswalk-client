from crosswalk_client.exceptions import MalformedThreshold


def validate_threshold_kwarg(function):
    def wrapper(*args, **kwargs):
        client = args[0]
        threshold = kwargs.get("threshold", client.threshold)
        if not isinstance(threshold, int):
            raise MalformedThreshold("Threshold should be an integer")
        if threshold < 0 or threshold > 100:
            raise MalformedThreshold("Threshold should be between 0 and 100")
        return function(*args, **kwargs)

    return wrapper
