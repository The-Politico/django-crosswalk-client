import uuid

import stringcase


def snake_case_keys(whatever_dict):
    """
    Converts keys in dict to snake case.
    """
    return {stringcase.snakecase(k): v for k, v in whatever_dict.items()}


class EntityObject(object):
    """
    Converts json returned form server into a proper entity object.
    """

    def update(self, update_attrs):
        entity = self.__client.update_by_id(self.uuid, update_attrs)
        self.__dict__ = entity.__dict__

    def delete(self):
        deleted = self.__client.delete_by_id(self.uuid)
        if deleted:
            self.__dict__ = {"uuid": self.uuid, "deleted": deleted}

    def set_alias_for(self, alias_for):
        entity = self.__client.alias_by_id(self.uuid, alias_for.uuid)
        self.__dict__ = entity.__dict__

    def remove_alias_for(self):
        entity = self.__client.alias_by_id(self.uuid, None)
        self.__dict__ = entity.__dict__

    def set_superseded_by(self, superseded_by):
        entity = self.__client.supersede_by_id(self.uuid, superseded_by.uuid)
        self.__dict__ = entity.__dict__

    def remove_superseded_by(self):
        entity = self.__client.supersede_by_id(self.uuid, None)
        self.__dict__ = entity.__dict__

    def __init__(self, response, client=None):
        entity = response.pop("entity", {})
        attributes = entity.pop("attributes", {})

        self.__dict__ = {
            **snake_case_keys(response),
            **snake_case_keys(entity),
            **snake_case_keys(attributes),
        }

        # Manually decode UUIDs, which are strings when decoded from json
        self.uuid = uuid.UUID(self.uuid)
        if self.superseded_by:
            self.superseded_by = uuid.UUID(self.superseded_by)
        if self.alias_for:
            self.alias_for = uuid.UUID(self.alias_for)

        self.__client = client

    def __repr__(self):
        return f"<Crosswalk Entity: {str(self.uuid)[:6]}...>"
