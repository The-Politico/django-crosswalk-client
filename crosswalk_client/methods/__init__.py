from .client.client_check import ClientCheck
from .client.set_domain import SetDomain
from .client.set_scorer import SetScorer
from .client.set_threshold import SetThreshold

from .domain.create_domain import CreateDomain
from .domain.delete_domain import DeleteDomain
from .domain.get_domain import GetDomain
from .domain.get_domains import GetDomains
from .domain.update_domain import UpdateDomain

from .entity.alias_by_id import AliasById
from .entity.alias_or_create import AliasOrCreate
from .entity.best_match_or_create import BestMatchOrCreate
from .entity.best_match import BestMatch
from .entity.bulk_create import BulkCreate
from .entity.delete_by_id import DeleteById
from .entity.delete_match import DeleteMatch
from .entity.get_entities import GetEntities
from .entity.get_entity import GetEntity
from .entity.match_or_create import MatchOrCreate
from .entity.match import Match
from .entity.supersede_by_id import SupersedeById
from .entity.update_by_id import UpdateById
from .entity.update_match import UpdateMatch


class ClientMethods(
    # client methods
    ClientCheck,
    SetScorer,
    SetDomain,
    SetThreshold,
    # domain methods
    CreateDomain,
    DeleteDomain,
    GetDomain,
    GetDomains,
    UpdateDomain,
    # entity methods
    AliasById,
    AliasOrCreate,
    BestMatchOrCreate,
    BestMatch,
    BulkCreate,
    DeleteById,
    DeleteMatch,
    GetEntities,
    GetEntity,
    MatchOrCreate,
    Match,
    SupersedeById,
    UpdateById,
    UpdateMatch,
):
    pass
