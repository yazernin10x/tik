from src.utils import reassign_module_names

from ._level import LevelCreate, LevelRead, LevelUpdate
from ._category import CategoryCreate, CategoryRead, CategoryUpdate
from ._status import StatusCreate, StatusRead, StatusUpdate
from ._comment import (
    CommentCreate,
    CommentRead,
    CommentReadLight,
    CommentUpdate,
)
from ._user import UserCreate, UserRead, UserReadLight, UserUpdate
from ._project import ProjectCreate, ProjectRead, ProjectReadLight, ProjectUpdate
from ._ticket import TicketCreate, TicketRead, TicketReadLight, TicketUpdate

LevelRead.model_rebuild()
CategoryRead.model_rebuild()
StatusRead.model_rebuild()
UserRead.model_rebuild()
CommentRead.model_rebuild()
ProjectRead.model_rebuild()
TicketRead.model_rebuild()

__all__ = [
    "LevelCreate",
    "LevelRead",
    "LevelUpdate",
    "CategoryCreate",
    "CategoryRead",
    "CategoryUpdate",
    "StatusCreate",
    "StatusRead",
    "StatusUpdate",
    "CommentCreate",
    "CommentRead",
    "CommentReadLight",
    "CommentUpdate",
    "ProjectCreate",
    "ProjectRead",
    "ProjectReadLight",
    "ProjectUpdate",
    "TicketCreate",
    "TicketRead",
    "TicketReadLight",
    "TicketUpdate",
    "UserCreate",
    "UserRead",
    "UserReadLight",
    "UserUpdate",
]

reassign_module_names(__name__, locals())
