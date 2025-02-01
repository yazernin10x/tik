from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError, InvalidRequestError
from sqlalchemy.orm.exc import StaleDataError

from src.backend.config import LOG_ERROR


async def integrity_error(request: Request, exc: IntegrityError) -> Response:
    request.state.db.rollback()
    LOG_ERROR.error(f"Integrity error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": f"Integrity error: {str(exc)}",
        },
    )


async def operational_error(request: Request, exc: OperationalError) -> Response:
    request.state.db.rollback()
    LOG_ERROR.error(f"Operational error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status_code": 500, "message": f"Operational error: {str(exc)}"},
    )


async def invalid_request_error(request: Request, exc: InvalidRequestError) -> Response:
    request.state.db.rollback()
    LOG_ERROR.error(f"Invalid error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"status_code": 400, "message": f"Invalid request error: {str(exc)}"},
    )


async def stale_data_error(request: Request, exc: StaleDataError) -> Response:
    request.state.db.rollback()
    LOG_ERROR.error(f"Stale data error: {str(exc)}")
    return JSONResponse(
        status_code=409,
        content={"status_code": 400, "message": f"Stale data error: {str(exc)}"},
    )
