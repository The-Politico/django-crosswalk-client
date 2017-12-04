from .client_check import ClientCheck
from .bulk_create import BulkCreate
from .delete_domain import DeleteDomain
from .create_domain import CreateDomain


class ClientMethods(
    ClientCheck,
    BulkCreate,
    DeleteDomain,
    CreateDomain,
):
    pass
