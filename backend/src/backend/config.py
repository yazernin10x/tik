import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger


def create_log(file, level):
    name = file.split(".")[0]
    log = logger.bind(**{name: ""})
    log.add(
        LOG_DIR / file,
        level=level,
        rotation="500 KB",
        retention="5 days",
        filter=lambda record: name in record["extra"],
    )
    return log


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configuration de la base de données
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR / 'tik.db'}"
ENGINE = create_engine(SQLALCHEMY_DATABASE_URL)  # , echo=True
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


# Congiguration des logs
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_APP = create_log("app.log", "INFO")  # INFO, WARNING
LOG_ERROR = create_log("errors.log", "ERROR")  # ERROR, CRITICAL
LOG_ACCESS = create_log("access.log", "INFO")  # INFO
LOG_DEBUG = create_log("debug.log", "DEBUG")  # DEBUG


# Capture automatique des exceptions
def log_exceptions(exc_type, exc_value, tb):
    logger.exception(
        "An unhandled exception was raised", exc_info=(exc_type, exc_value, tb)
    )


sys.excepthook = log_exceptions
