class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class ConfigError(BaseError):
    pass


class BadResponse(BaseError):
    pass


class BadRequest(BaseError):
    pass


class MalformedQuery(BaseError):
    pass


class MalformedBlockAttributes(BaseError):
    pass


class MalformedCreateAttributes(BaseError):
    pass


class MalformedUpdateAttributes(BaseError):
    pass


class MissingThreshold(BaseError):
    pass


class MalformedThreshold(BaseError):
    pass


class MissingScorer(BaseError):
    pass


class MalformedScorer(BaseError):
    pass


class MissingDomain(BaseError):
    pass


class MalformedDomain(BaseError):
    pass


class MalformedUUID(BaseError):
    pass


class ProtectedDomainError(BaseError):
    pass


class ProtectedEntitynError(BaseError):
    pass


class UnspecificDeleteRequestError(BaseError):
    pass


class UnspecificQueryError(BaseError):
    pass


class CreateEntityError(BaseError):
    pass


class UpdateEntityError(BaseError):
    pass


class EntityNotFoundError(BaseError):
    pass
