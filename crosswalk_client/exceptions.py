class ConfigError(Exception):
    def __init__(self, message):
        self.message = message


class BadResponse(Exception):
    def __init__(self, message):
        self.message = message
