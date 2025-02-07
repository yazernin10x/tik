from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.backend.config import DEBUG, LOG_ERROR


async def handle_error(
    request: Request, exc: Exception, error_type: str
) -> JSONResponse:
    """Handle errors and return an appropriate JSON response.

    Parameters
    ----------
    request : Request
        The request object.
    exc : Exception
        The exception that was raised.
    error_type : str
        A string indicating the type of error.

    Returns
    -------
    JSONResponse
        A JSON response with the appropriate status code and error message.

    Raises
    ------
    Exception
        If DEBUG is True, the original exception is re-raised.
    """
    request.state.db.rollback()
    LOG_ERROR.error(f"{error_type} error: {exc}")

    if DEBUG:
        raise

    if not hasattr(exc, "status_code") and "validation".lower() in str(exc):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        status_code = exc.status_code

    return JSONResponse(status_code=status_code, content=str(exc))
