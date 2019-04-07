from crosswalk_client.exceptions import MalformedScorer, MissingScorer

VALID_SCORERS = [
    "fuzzywuzzy.default_process",
    "fuzzywuzzy.partial_ratio_process",
    "fuzzywuzzy.token_sort_ratio_process",
    "fuzzywuzzy.token_set_ratio_process",
]


def validate_required_scorer(function):
    """
    Validates a threshold.
    """

    def wrapper(*args, **kwargs):
        list_args = list(args)
        try:
            scorer = list_args[1]
        except IndexError:
            raise MissingScorer("Must pass a scorer")
        if not isinstance(scorer, str):
            raise MalformedScorer("Scorer must be a string")
        if scorer not in VALID_SCORERS:
            raise MalformedScorer("Invalid scorer")
        return function(*args, **kwargs)

    return wrapper
