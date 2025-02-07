from fastapi import Request
from pydantic import ValidationError
from fastapi.responses import JSONResponse

from src.handlers.utils import handle_error


async def validation_error_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    return await handle_error(request, exc, "Validation")
