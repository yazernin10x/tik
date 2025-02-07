import pytest
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import Level
from src.exceptions import NotFoundException


@pytest.mark.dependency(name="create-level")
class TestCreateLevel:
    def test_201_created(self, app: TestClient, db: Session):
        data = {"label": "Test Level"}
        rep = app.post("/levels/", json=data)

        assert rep.status_code == status.HTTP_201_CREATED

        rep_data = rep.json()
        assert rep_data["label"] == data["label"]
        assert "id" in rep_data

        level = db.query(Level).filter(Level.id == rep_data["id"]).first()
        assert level is not None
        assert level.label == data["label"]


@pytest.mark.dependency(depends=["create-level"])
class TestGetLevel:
    def test_200_ok(self, app: TestClient, db: Session):
        level_data = {"label": "Test Level"}
        rep_create = app.post("/levels/", json=level_data).json()
        rep_get = app.get(f"/levels/{rep_create["id"]}")

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_create

    def test_404_not_found(self, app: TestClient, db: Session):
        level_id = 1
        msg = f"Level with ID {level_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get(f"/levels/{level_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-level"])
class TestGetLevels:
    def test_200_ok(self, app: TestClient, db: Session):
        level_data_1 = {"label": "Test Level 1"}
        level_data_2 = {"label": "Test Level 2"}
        rep_create_1 = app.post("/levels/", json=level_data_1).json()
        rep_create_2 = app.post("/levels/", json=level_data_2).json()

        rep_get = app.get("/levels/")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == [rep_create_1, rep_create_2]

    def test_404_not_found(self, app: TestClient, db: Session):
        msg = "No levels found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get("/levels/")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-level"])
class TestUpdateLevel:
    def test_200_ok(self, app: TestClient, db: Session):
        level_data = {"label": "Test Level"}
        rep_post = app.post("/levels/", json=level_data).json()

        new_data = {"label": "New label"}
        rep_get = app.put(f"/levels/{rep_post['id']}", json=new_data)

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post | new_data

    def test_200_ok_empty_data(self, app: TestClient, db: Session):
        level_data = {"label": "Test Level"}
        rep_post = app.post("/levels/", json=level_data).json()
        rep_get = app.put(f"/levels/{rep_post['id']}", json={})

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post

    def test_404_not_found(self, app: TestClient, db: Session):
        level_id = 1
        msg = f"Level with ID {level_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            new_data = {"label": "New label"}
            rep = app.put(f"/levels/{level_id}", json=new_data)
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-level"])
class TestDeleteLevel:
    def test_200_ok(self, app: TestClient, db: Session):
        level_data = {"label": "Test Level"}
        rep_poste = app.post("/levels/", json=level_data).json()
        rep_get = app.delete(f"/levels/{rep_poste["id"]}")

        assert rep_get.status_code == status.HTTP_200_OK

    def test_404_not_found(self, app: TestClient, db: Session):
        level_id = 1
        msg = f"Level with ID {level_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.delete(f"/levels/{level_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg
