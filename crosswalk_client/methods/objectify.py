def snake_case_keys(spaced_dict):
    """
    Converts keys in dict to snakecase.
    """
    return {
        k.replace(' ', '_').replace('-', '_'): v
        for k, v in spaced_dict.items()
    }


class AttributeObject(object):
    """
    Converts json returned form server into proper
    objects for entities and domains.
    """
    def __init__(self, responseDict):
        entity = responseDict.pop('entity', {})
        attributes = entity.pop('attributes', {})
        self.__dict__ = {
            **snake_case_keys(responseDict),
            **snake_case_keys(entity),
            **snake_case_keys(attributes)
        }
