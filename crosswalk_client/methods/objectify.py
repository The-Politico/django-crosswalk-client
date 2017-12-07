class AttributeObject(object):
    """Converts attribute dicts to proper objects."""
    def __init__(self, response):
        entity = response.pop('entity')
        attributes = entity.pop('attributes')
        self.__dict__ = {
            **response,
            **entity,
            **attributes
        }
