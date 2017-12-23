import json
from uuid import UUID


class CustomEncoder(json.JSONEncoder):
    """
    Extension of custom encoder that encodes UUIDs.
    """
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


def encode(obj):
    """
    Uses CustomEncoder to dump JSON with UUIDs.
    """
    return json.dumps(obj, cls=CustomEncoder)
