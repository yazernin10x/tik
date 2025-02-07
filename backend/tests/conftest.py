import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient


from main import app
from src.models import Base
from src.backend.config import ENGINE, SESSION_LOCAL


@pytest.fixture(name="db", scope="function")
def db_session():
    Base.metadata.create_all(ENGINE)
    session = SESSION_LOCAL()
    yield session
    session.close()
    Base.metadata.drop_all(ENGINE)


@pytest.fixture(name="app", scope="module")
def test_app():
    client = TestClient(app)
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
def user_data(app: TestClient, db: Session) -> dict:
    return {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "role": "user",
        "password": "SecurePass123",
    }


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
