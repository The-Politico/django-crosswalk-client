from .methods import ClientMethods


class Client(ClientMethods):
    def __init__(
        self,
        token,
        service_address,
        domain=None,
        create_threshold=80,
        scorer='crosswalk.scorers.fuzzywuzzy.default_process',
    ):
        self.token = token
        self.service_address = service_address
        self.headers = {
            'Authorization': 'TOKEN {}'.format(self.token)
        }
        self.domain = domain
        self.create_threshold = create_threshold
        self.scorer = scorer
        self.client_check()
