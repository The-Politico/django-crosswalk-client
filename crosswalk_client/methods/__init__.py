from .client_check import ClientCheck
from .bulk_create import BulkCreate
from .delete_domain import DeleteDomain
from .create_domain import CreateDomain
from .best_match import BestMatch
from .set_domain import SetDomain
from .list_domains import ListDomains
from .best_match_or_create import BestMatchOrCreate


class ClientMethods(
    ClientCheck,
    BulkCreate,
    DeleteDomain,
    CreateDomain,
    BestMatch,
    BestMatchOrCreate,
    SetDomain,
    ListDomains,
):
    pass
