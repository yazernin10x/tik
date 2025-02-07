from fastapi import Request
from src.backend.config import SESSION_LOCAL
from starlette.middleware.base import BaseHTTPMiddleware


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = SESSION_LOCAL()
        request.state.db = db
        try:
            response = await call_next(request)
        finally:
            db.close()
        return response
