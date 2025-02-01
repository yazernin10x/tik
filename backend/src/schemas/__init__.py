from src.utils import reassign_module_names

from ._level import LevelCreate, LevelRead

__all__ = ["LevelCreate", "LevelRead"]

reassign_module_names(__name__, locals())
