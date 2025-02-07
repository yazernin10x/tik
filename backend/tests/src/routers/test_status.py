import pytest
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import Status
from src.exceptions import NotFoundException


@pytest.mark.dependency(name="create-status")
class TestCreateStatus:
    def test_201_created(self, app: TestClient, db: Session):
        data = {"label": "Test Status"}
        rep = app.post("/statuses/", json=data)

        assert rep.status_code == status.HTTP_201_CREATED

        rep_data = rep.json()
        assert rep_data["label"] == data["label"]
        assert "id" in rep_data

        status_ = db.query(Status).filter(Status.id == rep_data["id"]).first()
        assert status_ is not None
        assert status_.label == data["label"]


@pytest.mark.dependency(depends=["create-status"])
class TestGetStatus:
    def test_200_ok(self, app: TestClient, db: Session):
        status_data = {"label": "Test Status"}
        rep_create = app.post("/statuses/", json=status_data).json()
        rep_get = app.get(f"/statuses/{rep_create["id"]}")

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_create

    def test_404_not_found(self, app: TestClient, db: Session):
        status_id = 1
        msg = f"Status with ID {status_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get(f"/statuses/{status_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-status"])
class TestGetStatuses:
    def test_200_ok(self, app: TestClient, db: Session):
        status_data_1 = {"label": "Test Status 1"}
        status_data_2 = {"label": "Test Status 2"}
        rep_create_1 = app.post("/statuses/", json=status_data_1).json()
        rep_create_2 = app.post("/statuses/", json=status_data_2).json()

        rep_get = app.get("/statuses/")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == [rep_create_1, rep_create_2]

    def test_404_not_found(self, app: TestClient, db: Session):
        msg = "No statuses found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get("/statuses/")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-status"])
class TestUpdateStatus:
    def test_200_ok(self, app: TestClient, db: Session):
        status_data = {"label": "Test Status"}
        rep_post = app.post("/statuses/", json=status_data).json()

        new_data = {"label": "New label"}
        rep_get = app.put(f"/statuses/{rep_post['id']}", json=new_data)

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post | new_data

    def test_200_ok_empty_data(self, app: TestClient, db: Session):
        status_data = {"label": "Test Status"}
        rep_post = app.post("/statuses/", json=status_data).json()
        rep_get = app.put(f"/statuses/{rep_post['id']}", json={})

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post

    def test_404_not_found(self, app: TestClient, db: Session):
        status_id = 1
        msg = f"Status with ID {status_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            new_data = {"label": "New label"}
            rep = app.put(f"/statuses/{status_id}", json=new_data)
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-status"])
class TestDeleteStatus:
    def test_200_ok(self, app: TestClient, db: Session):
        status_data = {"label": "Test Status"}
        rep_poste = app.post("/statuses/", json=status_data).json()
        rep_get = app.delete(f"/statuses/{rep_poste["id"]}")

        assert rep_get.status_code == status.HTTP_200_OK

    def test_404_not_found(self, app: TestClient, db: Session):
        status_id = 1
        msg = f"Status with ID {status_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.delete(f"/statuses/{status_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg
