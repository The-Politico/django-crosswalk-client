class AttributeObject(object):
    """
    Converts json returned form server into proper
    objects for entities and domains.
    """
    def __init__(self, responseDict):
        entity = responseDict.pop('entity', {})
        attributes = entity.pop('attributes', {})
        self.__dict__ = {
            **responseDict,
            **entity,
            **attributes
        }
