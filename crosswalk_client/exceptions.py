class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class ConfigError(BaseError):
    pass


class BadResponse(BaseError):
    pass


class ProtectedDomainError(BaseError):
    pass


class ProtectedEntitynError(BaseError):
    pass


class UnspecificDeleteRequestError(BaseError):
    pass


class CreateEntityError(BaseError):
    pass
