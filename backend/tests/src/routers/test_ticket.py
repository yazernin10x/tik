import pytest
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models._ticket import Ticket
from src.exceptions import NotFoundException


@pytest.mark.dependency(name="create-ticket")
class TestCreateTicket:
    def test_201_created(self, app: TestClient, db: Session, ticket_data: dict) -> None:
        data = ticket_data
        rep = app.post("/tickets/", json=data)

        assert rep.status_code == status.HTTP_201_CREATED

        rep_data = rep.json()
        assert rep_data["title"] == data["title"]
        assert rep_data["description"] == data["description"]
        assert rep_data["creator"]["id"] == data["creator_id"]
        assert rep_data["project"]["id"] == data["project_id"]
        assert rep_data["status"]["id"] == data["status_id"]
        assert rep_data["category"]["id"] == data["category_id"]
        assert rep_data["level"]["id"] == data["level_id"]
        assert "id" in rep_data

        ticket = db.query(Ticket).filter(Ticket.id == rep_data["id"]).first()
        assert ticket is not None
        assert ticket.title == data["title"]
        assert ticket.description == data["description"]
        assert ticket.creator.id == data["creator_id"]
        assert ticket.project.id == data["project_id"]
        assert ticket.status.id == data["status_id"]
        assert ticket.category.id == data["category_id"]
        assert ticket.level.id == data["level_id"]


@pytest.mark.dependency(depends=["create-ticket"])
class TestGetTicket:
    def test_200_ok(self, app: TestClient, db: Session, ticket_data: dict) -> None:
        rep_create = app.post("/tickets/", json=ticket_data).json()
        rep_get = app.get(f"/tickets/{rep_create['id']}")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_create

    def test_404_not_found(self, app: TestClient, db: Session):
        ticket_id = 1
        msg = f"Ticket with ID {ticket_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get(f"/tickets/{ticket_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-ticket"])
class TestGetTickets:
    def test_200_ok(self, app: TestClient, db: Session, ticket_data: dict) -> None:
        ticket_data_1 = {
            "title": "Ticket 1",
            "description": "Description of Ticket 1",
            "creator_id": ticket_data["creator_id"],
            "project_id": ticket_data["project_id"],
            "status_id": ticket_data["status_id"],
            "category_id": ticket_data["category_id"],
            "level_id": ticket_data["level_id"],
        }
        rep_create_1 = app.post("/tickets/", json=ticket_data).json()
        rep_create_2 = app.post("/tickets/", json=ticket_data_1).json()

        rep_get = app.get("/tickets/")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == [rep_create_1, rep_create_2]

    def test_404_not_found(self, app: TestClient, db: Session) -> None:
        msg = "No tickets found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get("/tickets/")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-ticket"])
class TestUpdateTicket:
    def test_200_ok_non_empty_data(
        self, app: TestClient, db: Session, ticket_data: dict
    ) -> None:
        rep_post = app.post("/tickets/", json=ticket_data).json()

        new_data = {"title": "Updated Ticket", "description": "Updated description"}
        rep_put = app.put(f"/tickets/{rep_post['id']}", json=new_data)

        assert rep_put.status_code == status.HTTP_200_OK
        assert rep_put.json()["title"] == new_data["title"]
        assert rep_put.json()["description"] == new_data["description"]

    def test_200_ok_empty_data(
        self, app: TestClient, db: Session, ticket_data: dict
    ) -> None:
        rep_post = app.post("/tickets/", json=ticket_data).json()
        rep_get = app.put(f"/tickets/{rep_post['id']}", json={})

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post

    def test_404_not_found(self, app: TestClient, db: Session):
        ticket_id = 1
        new_data = {"title": "Updated Ticket", "description": "Updated description"}
        msg = f"Ticket with ID {ticket_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.put(f"/tickets/{ticket_id}", json=new_data)
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-ticket"])
class TestDeleteTicket:
    def test_200_ok(self, app: TestClient, db: Session, ticket_data: dict):
        rep_post = app.post("/tickets/", json=ticket_data).json()
        rep_delete = app.delete(f"/tickets/{rep_post['id']}")

        assert rep_delete.status_code == status.HTTP_200_OK

    def test_404_not_found(self, app: TestClient, db: Session):
        ticket_id = 1
        msg = f"Ticket with ID {ticket_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.delete(f"/tickets/{ticket_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg
