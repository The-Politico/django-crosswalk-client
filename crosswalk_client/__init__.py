from .methods import ClientMethods


class Client(ClientMethods):
    def __init__(
        self,
        token,
        service_address,
        domain=None,
        create_threshold=80,
    ):
        self.token = token
        self.service_address = service_address
        self.headers = {
            'Authorization': 'TOKEN {}'.format(self.token)
        }
        self.domain = domain
        self.create_threshold = create_threshold
        self.client_check()
