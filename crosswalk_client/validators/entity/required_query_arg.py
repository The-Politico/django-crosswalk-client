from crosswalk_client.exceptions import MalformedQuery


def validate_required_query_arg(function):
    def wrapper(*args, **kwargs):
        query = args[1]
        if not isinstance(query, dict):
            raise MalformedQuery("Query should be a dictionary")
        if len(query.keys()) > 1:
            raise MalformedQuery(
                "Query should only include one key value pair"
            )
        if not isinstance(list(query.values())[0], str) or not isinstance(
            list(query.keys())[0], str
        ):
            raise MalformedQuery("Query key and value should be strings")
        return function(*args, **kwargs)

    return wrapper
