class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class ConfigError(BaseError):
    pass


class BadResponse(BaseError):
    pass


class ProtectedError(BaseError):
    pass
