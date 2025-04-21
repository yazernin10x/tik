from fastapi import FastAPI
from fastapi_pagination import add_pagination, set_page, set_params
from fastapi_pagination.default import Params
from fastapi_pagination.links.default import Page

from pydantic import ValidationError
from sqlalchemy.orm.exc import StaleDataError
from sqlalchemy.exc import IntegrityError, OperationalError, InvalidRequestError

from src.middlewares import DBSessionMiddleware
from src.exceptions import NotFoundException, CredentialsException
from src.handlers import (
    integrity_error_handler,
    operational_error_handler,
    invalid_request_error_handler,
    stale_data_error_handler,
    validation_error_handler,
    not_found_exception_handler,
    credentials_exception_handler,
)
from src.routers import (
    home,
    category,
    comment,
    project,
    status,
    ticket,
    user,
    level,
    auth,
)


# mypy: disable-error-code=arg-type


def create_app():
    app = FastAPI(title="TiK")

    set_page(Page)
    set_params(Params(page=1, size=50))
    add_pagination(app)

    # Middleware
    app.add_middleware(DBSessionMiddleware)

    # Gestion des erreurs
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(OperationalError, operational_error_handler)
    app.add_exception_handler(InvalidRequestError, invalid_request_error_handler)
    app.add_exception_handler(StaleDataError, stale_data_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(CredentialsException, credentials_exception_handler)

    # Inclusion des routes
    app.include_router(auth.router)
    app.include_router(home.router)
    app.include_router(category.router)
    app.include_router(comment.router)
    app.include_router(level.router)
    app.include_router(status.router)
    app.include_router(project.router)
    app.include_router(ticket.router)
    app.include_router(user.router)

    return app
