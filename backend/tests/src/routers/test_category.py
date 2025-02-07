import pytest
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import Category
from src.exceptions import NotFoundException


@pytest.mark.dependency(name="create-category")
class TestCreateCategory:
    def test_201_created(self, app: TestClient, db: Session):
        data = {"label": "Test Category"}
        rep = app.post("/categories/", json=data)

        assert rep.status_code == status.HTTP_201_CREATED

        rep_data = rep.json()
        assert rep_data["label"] == data["label"]
        assert "id" in rep_data

        category = db.query(Category).filter(Category.id == rep_data["id"]).first()
        assert category is not None
        assert category.label == data["label"]


@pytest.mark.dependency(depends=["create-category"])
class TestGetCategory:
    def test_200_ok(self, app: TestClient, db: Session):
        category_data = {"label": "Test Category"}
        rep_create = app.post("/categories/", json=category_data).json()
        rep_get = app.get(f"/categories/{rep_create["id"]}")

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_create

    def test_404_not_found(self, app: TestClient, db: Session):
        category_id = 1
        msg = f"Category with ID {category_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get(f"/categories/{category_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-category"])
class TestGetCategories:
    def test_200_ok(self, app: TestClient, db: Session):
        category_data_1 = {"label": "Test Category 1"}
        category_data_2 = {"label": "Test Category 2"}
        rep_create_1 = app.post("/categories/", json=category_data_1).json()
        rep_create_2 = app.post("/categories/", json=category_data_2).json()

        rep_get = app.get("/categories/")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == [rep_create_1, rep_create_2]

    def test_404_not_found(self, app: TestClient, db: Session):
        msg = "No categories found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get("/categories/")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-category"])
class TestUpdateCategory:
    def test_200_ok_non_empty_data(self, app: TestClient, db: Session):
        category_data = {"label": "Test Category"}
        rep_post = app.post("/categories/", json=category_data).json()

        new_data = {"label": "New label"}
        rep_get = app.put(f"/categories/{rep_post['id']}", json=new_data)

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post | new_data

    def test_200_ok_empty_data(self, app: TestClient, db: Session):
        category_data = {"label": "Test Category"}
        rep_post = app.post("/categories/", json=category_data).json()
        rep_get = app.put(f"/categories/{rep_post['id']}", json={})

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post

    def test_404_not_found(self, app: TestClient, db: Session):
        category_id = 1
        msg = f"Category with ID {category_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            new_data = {"label": "New label"}
            rep = app.put(f"/categories/{category_id}", json=new_data)
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-category"])
class TestDeleteCategory:
    def test_200_ok(self, app: TestClient, db: Session):
        category_data = {"label": "Test Category"}
        rep_poste = app.post("/categories/", json=category_data).json()
        rep_get = app.delete(f"/categories/{rep_poste["id"]}")

        assert rep_get.status_code == status.HTTP_200_OK

    def test_404_not_found(self, app: TestClient, db: Session):
        category_id = 1
        msg = f"Category with ID {category_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.delete(f"/categories/{category_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg
