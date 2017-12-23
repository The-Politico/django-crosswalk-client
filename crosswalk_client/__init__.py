from .methods import ClientMethods


class Client(ClientMethods):
    def __init__(
        self,
        token,
        service_address,
        domain=None,
        threshold=80,
        scorer='fuzzywuzzy.default_process',
    ):
        self.token = token
        self.service_address = service_address
        self.headers = {
            'Authorization': 'TOKEN {}'.format(self.token),
            'Content-Type': 'application/json',
        }
        self.domain = domain
        self.threshold = threshold
        self.scorer = scorer
        self.client_check()
