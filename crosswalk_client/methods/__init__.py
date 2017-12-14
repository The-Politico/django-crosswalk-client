from .client.client_check import ClientCheck
from .client.set_domain import SetDomain
from .client.set_scorer import SetScorer
from .client.set_threshold import SetThreshold

from .domain.create_domain import CreateDomain
from .domain.delete_domain import DeleteDomain
from .domain.update_domain import UpdateDomain
from .domain.get_domains import GetDomains

from .entity.bulk_create import BulkCreate
from .entity.best_match import BestMatch
from .entity.best_match_or_create import BestMatchOrCreate
from .entity.delete_match import DeleteMatch
from .entity.create_matched_alias import CreateMatchedAlias
from .entity.get_entities import GetEntities
from .entity.delete_by_id import DeleteById
from .entity.update_by_id import UpdateById
from .entity.update_match import UpdateMatch


class ClientMethods(
    ClientCheck,
    BulkCreate,
    DeleteDomain,
    CreateDomain,
    BestMatch,
    BestMatchOrCreate,
    SetScorer,
    SetDomain,
    SetThreshold,
    GetDomains,
    GetEntities,
    DeleteMatch,
    CreateMatchedAlias,
    DeleteById,
    UpdateById,
    UpdateMatch,
    UpdateDomain,
):
    pass
