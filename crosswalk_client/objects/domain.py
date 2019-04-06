class DomainObject(object):
    """
    Converts json returned form server into a proper domain object.
    """

    def update(self, update_attrs):
        domain = self.__client.update_domain(self.slug, update_attrs)
        self.__dict__ = domain.__dict__

    def set_parent(self, parent):
        domain = self.__client.update_domain(
            self.slug, {"parent": parent.slug}
        )
        self.__dict__ = domain.__dict__

    def remove_parent(self):
        domain = self.__client.update_domain(self.slug, {"parent": None})
        self.__dict__ = domain.__dict__

    def delete(self):
        deleted = self.__client.delete_domain(self.slug)
        if deleted:
            self.__dict__ = {"slug": self.slug, "deleted": deleted}

    def __init__(self, response, client=None):
        self.__dict__ = response
        self.__client = client

    def __repr__(self):
        return f"<Crosswalk Domain: {self.slug}>"
