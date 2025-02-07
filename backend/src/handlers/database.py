from fastapi import Request
from fastapi.responses import JSONResponse

from sqlalchemy.exc import DataError
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    InvalidRequestError,
    StatementError,
)
from sqlalchemy.orm.exc import StaleDataError, UnmappedInstanceError


from src.handlers.utils import handle_error
from src.exceptions import NotFoundException


async def not_found_exception_handler(
    request: Request, exc: NotFoundException
) -> JSONResponse:
    return await handle_error(request, exc, "Not found")


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    return await handle_error(request, exc, "Integrity")


async def operational_error_handler(
    request: Request, exc: OperationalError
) -> JSONResponse:
    return await handle_error(request, exc, "Operational")


async def invalid_request_error_handler(
    request: Request, exc: InvalidRequestError
) -> JSONResponse:
    return await handle_error(request, exc, "Invalid")


async def stale_data_error_handler(
    request: Request, exc: StaleDataError
) -> JSONResponse:
    return await handle_error(request, exc, "Stale data")


async def unmapped_instance_error_handler(
    request: Request, exc: UnmappedInstanceError
) -> JSONResponse:
    return await handle_error(request, exc, "Unmapped instance")


async def statement_error_handler(
    request: Request, exc: StatementError
) -> JSONResponse:
    return await handle_error(request, exc, "Statement")


async def data_error_handler(request: Request, exc: DataError) -> JSONResponse:
    return await handle_error(request, exc, "Data")
