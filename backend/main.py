from fastapi import FastAPI
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError, InvalidRequestError
from sqlalchemy.orm.exc import StaleDataError

from src.models import Base
from src.routers import level
from src.backend.config import ENGINE
from src.middlewares import db_session
from src.handlers import (
    integrity_error,
    operational_error,
    invalid_request_error,
    stale_data_error,
)
from src.handlers import validation_error_handler

# mypy: disable-error-code=arg-type

Base.metadata.create_all(bind=ENGINE)

app = FastAPI()

app.include_router(level.router)

# Enregistrer le middleware
app.middleware("http")(db_session)

# Enregistrer les gestionnaires d'exceptions globaux
app.add_exception_handler(IntegrityError, integrity_error)
app.add_exception_handler(OperationalError, operational_error)
app.add_exception_handler(InvalidRequestError, invalid_request_error)
app.add_exception_handler(StaleDataError, stale_data_error)
app.add_exception_handler(ValidationError, validation_error_handler)


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API FastAPI !"}
