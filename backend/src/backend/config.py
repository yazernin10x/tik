"""Configuration file for the backend.

Attributes:
    BASE_DIR (Path): The base directory of the project, resolved to the third parent directory of this file.
    DEBUG (bool): Flag to enable or disable debug mode.
    TEST (bool): Flag to indicate if the application is in test mode.
    SQLALCHEMY_DATABASE_URL (str): The database URL for SQLAlchemy, using SQLite. Points to 'tests/test.db' if TEST is True, otherwise 'database.db'.
    ENGINE (Engine): The SQLAlchemy engine created with the database URL.
    SESSION_LOCAL (sessionmaker): The SQLAlchemy session factory.
    LOG_DIR (Path): The directory where log files will be stored.
    LOG_APP (Logger): Logger for application logs with INFO level.
                    Handles general application logs, including informational and warning messages.
    LOG_ERROR (Logger): Logger for error logs with ERROR level.
                        Handles error logs, including error and critical messages.
    LOG_ACCESS (Logger): Logger for access logs with INFO level.
                        Handles access logs, including informational messages about access events.
    LOG_DEBUG (Logger): Logger for debug logs with DEBUG level.
                        Handles debug logs, including detailed debug information.
Functions:
    create_log(file: str, level: str) -> Logger:
        Creates and configures a logger for a specific file and log level.
    log_exceptions(exc_type, exc_value, tb):
        Logs unhandled exceptions using the logger.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

# Sécurité JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

DEBUG = True
TEST = True

# Database configuration
SQLALCHEMY_DATABASE_URL = (
    f"sqlite:///{BASE_DIR}/{'tests/test.db' if TEST else 'database.db'}"
)
ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


# Log configuration
def create_log(filename, level):
    log_file = LOG_DIR / filename

    if not log_file.exists():
        log_file.touch()

    name = filename.split(".")[0]
    log = logger.bind(**{name: ""})
    log.add(
        LOG_DIR / filename,
        level=level,
        rotation="500 KB",
        retention="5 days",
        filter=lambda record: name in record["extra"],
    )
    return log


LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_APP = create_log("app.log", "INFO")
LOG_ERROR = create_log("errors.log", "ERROR")
LOG_ACCESS = create_log("access.log", "INFO")
LOG_DEBUG = create_log("debug.log", "DEBUG")


def log_exceptions(exc_type, exc_value, tb):
    logger.exception(
        "An unhandled exception was raised", exc_info=(exc_type, exc_value, tb)
    )


sys.excepthook = log_exceptions
