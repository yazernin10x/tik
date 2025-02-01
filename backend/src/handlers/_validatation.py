from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def validation_error_handler(request: Request, exc: ValidationError):
    request.state.db.rollback()
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "errors": exc.errors()},
    )
