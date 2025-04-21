from typing import Any
import pytest
from sqlalchemy import create_engine
from src.routers.auth import create_access_token
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient


from app import create_app
from src.models import Base, User
from src.exceptions import NotFoundException
from src.backend.config import ENGINE, SESSION_LOCAL, SQLALCHEMY_DATABASE_URL
from sqlalchemy.orm import sessionmaker

USER_PASSWORD = "SecurePass123"
USER_NAME = "johndoe"
USER_EMAIL = "yazernin10x@gmail.com"


@pytest.fixture(name="db", scope="function")
def db_session():

    # ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # noqa: F811
    # session = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    Base.metadata.create_all(ENGINE)
    db = SESSION_LOCAL()
    yield db
    db.close()
    Base.metadata.drop_all(ENGINE)


@pytest.fixture(name="app", scope="module")
def test_app():
    client = TestClient(create_app())
    yield client


@pytest.fixture(scope="function")
def status_data(app: TestClient, db: Session) -> dict:
    return {"label": "Open"}


@pytest.fixture(scope="function")
def category_data(app: TestClient, db: Session) -> dict:
    return {"label": "Bug"}


@pytest.fixture(scope="function")
def level_data(app: TestClient, db: Session) -> dict:
    return {"label": "High"}


@pytest.fixture(scope="function")
def user_data() -> dict:
    return {
        "first_name": "John",
        "last_name": "Doe",
        "username": USER_NAME,
        "email": USER_EMAIL,
        "role": "user",
        "password": USER_PASSWORD,
    }


@pytest.fixture(name="user", scope="function")
def create_user(app: TestClient, db: Session, user_data: dict) -> User:
    app.post("/users/", json=user_data).json()
    user = db.query(User).filter(User.username == user_data["username"]).first()
    if user is None:
        raise NotFoundException("User not found")
    return user


@pytest.fixture(name="user_session", scope="function")
def create_user_session(app: TestClient, user: User) -> dict[str, Any]:
    response = app.post(
        "/auth/login",
        data={"username": user.username, "password": USER_PASSWORD},
    )

    token = response.json().get("access_token")
    token_type = response.json().get("token_type")
    headers = {"Authorization": f"{token_type} {token}"}
    return {"user": user, "token": token, "headers": headers}


@pytest.fixture(scope="function")
def project_data(app: TestClient, db: Session, user_data: dict) -> dict:
    user_data = app.post("/users/", json=user_data).json()
    return {
        "label": "Project Alpha",
        "description": "Description of Project Alpha",
        "creator_id": user_data["id"],
    }


@pytest.fixture(scope="function")
def ticket_data(
    app: TestClient,
    db: Session,
    project_data: dict,
    status_data: dict,
    category_data: dict,
    level_data: dict,
) -> dict:
    project_data = app.post("/projects/", json=project_data).json()
    status_data = app.post("/statuses/", json=status_data).json()
    category_data = app.post("/categories/", json=category_data).json()
    level_data = app.post("/levels/", json=level_data).json()

    return {
        "title": "Ticket 1",
        "description": "Description of Ticket 1",
        "creator_id": project_data["creator"]["id"],
        "project_id": project_data["id"],
        "status_id": status_data["id"],
        "category_id": category_data["id"],
        "level_id": level_data["id"],
    }


@pytest.fixture(scope="function")
def comment_data(app: TestClient, db: Session, ticket_data: dict) -> dict:
    ticket_data = app.post("/tickets/", json=ticket_data).json()
    return {
        "creator_id": ticket_data["creator"]["id"],
        "ticket_id": ticket_data["id"],
        "content": "Comment of Ticket 1",
    }
