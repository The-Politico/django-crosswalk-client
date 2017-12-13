from .client_check import ClientCheck
from .bulk_create import BulkCreate
from .delete_domain import DeleteDomain
from .create_domain import CreateDomain
from .best_match import BestMatch
from .set_domain import SetDomain
from .get_domains import GetDomains
from .best_match_or_create import BestMatchOrCreate
from .delete_match import DeleteMatch
from .create_matched_alias import CreateMatchedAlias
from .get_entities import GetEntities
from .delete_by_id import DeleteById
from .update_by_id import UpdateById
from .update_match import UpdateMatch


class ClientMethods(
    ClientCheck,
    BulkCreate,
    DeleteDomain,
    CreateDomain,
    BestMatch,
    BestMatchOrCreate,
    SetDomain,
    GetDomains,
    GetEntities,
    DeleteMatch,
    CreateMatchedAlias,
    DeleteById,
    UpdateById,
    UpdateMatch,
):
    pass
