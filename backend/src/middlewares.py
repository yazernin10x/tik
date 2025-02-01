from fastapi import Request
from src.backend.config import SESSION_LOCAL


async def db_session(request: Request, call_next):
    db = SESSION_LOCAL()
    request.state.db = db
    try:
        response = await call_next(request)
    finally:
        db.close()
    return response
