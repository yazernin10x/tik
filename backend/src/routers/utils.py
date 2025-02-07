from src.exceptions import NotFoundException

from src.backend.config import LOG_APP


def raise_not_found_if_absent(item: object, message: str):
    if not item:
        LOG_APP.warning(message)
        raise NotFoundException(message)
