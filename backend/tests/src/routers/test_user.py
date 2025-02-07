import pytest
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import User
from src.exceptions import NotFoundException


@pytest.mark.dependency(name="create-user")
class TestCreateUser:
    def test_201_created(self, app: TestClient, db: Session, user_data: dict):
        data = user_data
        rep = app.post("/users/", json=data)

        assert rep.status_code == status.HTTP_201_CREATED

        rep_data = rep.json()
        assert rep_data["username"] == data["username"]
        assert rep_data["email"] == data["email"]
        assert rep_data["first_name"] == data["first_name"]
        assert rep_data["last_name"] == data["last_name"]
        assert rep_data["role"] == data["role"]
        assert "id" in rep_data

        user = db.query(User).filter(User.id == rep_data["id"]).first()
        assert user is not None
        assert user.username == data["username"]
        assert user.email == data["email"]
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.role == data["role"]
        assert user._password != data["password"]
        assert user.verify_password(data["password"])


@pytest.mark.dependency(depends=["create-user"])
class TestGetUser:
    def test_200_ok(self, app: TestClient, db: Session, user_data: dict):
        rep_create = app.post("/users/", json=user_data).json()
        rep_get = app.get(f"/users/{rep_create['id']}")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_create

    def test_404_not_found(self, app: TestClient, db: Session):
        user_id = 1
        msg = f"User with ID {user_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get(f"/users/{user_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-user"])
class TestGetAllUsers:
    def test_200_ok(self, app: TestClient, db: Session, user_data: dict):
        user_data_1 = {
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "janedoe",
            "email": "janedoe@example.com",
            "role": "user",
            "password": "SecurePass123",
        }
        rep_create_1 = app.post("/users/", json=user_data).json()
        rep_create_2 = app.post("/users/", json=user_data_1).json()

        response = app.get("/users/?page=1&size=10")
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["total"] == 2
        assert response_data["page"] == 1
        assert response_data["size"] == 10
        assert len(response_data["items"]) == 2
        assert response_data["items"] == [rep_create_1, rep_create_2]

    def test_404_not_found(self, app: TestClient, db: Session):
        msg = "No users found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get("/users/?page=1&size=10")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-user"])
class TestUpdateUser:
    def test_200_ok(self, app: TestClient, db: Session, user_data: dict):
        rep_post = app.post("/users/", json=user_data).json()
        new_data = {"first_name": "Jane", "last_name": "Smith"}
        rep_put = app.put(f"/users/{rep_post['id']}", json=new_data)

        assert rep_put.status_code == status.HTTP_200_OK
        assert rep_put.json()["first_name"] == new_data["first_name"]
        assert rep_put.json()["last_name"] == new_data["last_name"]

    def test_200_ok_empty_data(self, app: TestClient, db: Session, user_data: dict):
        rep_post = app.post("/users/", json=user_data).json()
        rep_get = app.put(f"/users/{rep_post['id']}", json={})

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post

    def test_404_not_found(self, app: TestClient, db: Session):
        user_id = 1
        new_data = {"first_name": "Jane", "last_name": "Smith"}
        msg = f"User with ID {user_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.put(f"/users/{user_id}", json=new_data)
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-user"])
class TestDeleteUser:
    def test_200_ok(self, app: TestClient, db: Session, user_data: dict):
        rep_post = app.post("/users/", json=user_data).json()
        rep_delete = app.delete(f"/users/{rep_post['id']}")

        assert rep_delete.status_code == status.HTTP_200_OK

    def test_404_not_found(self, app: TestClient, db: Session):
        user_id = 1
        msg = f"User with ID {user_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.delete(f"/users/{user_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg
