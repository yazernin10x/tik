import pytest
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import Project
from src.exceptions import NotFoundException


@pytest.mark.dependency(name="create-project")
class TestCreateProject:
    def test_201_created(self, app: TestClient, db: Session, project_data: dict):
        data = project_data
        rep = app.post("/projects/", json=data)

        assert rep.status_code == status.HTTP_201_CREATED

        rep_data = rep.json()
        assert rep_data["label"] == data["label"]
        assert rep_data["description"] == data["description"]
        assert "id" in rep_data

        project = db.query(Project).filter(Project.id == rep_data["id"]).first()
        assert project is not None
        assert project.label == data["label"]
        assert project.description == data["description"]


@pytest.mark.dependency(depends=["create-project"])
class TestGetProject:
    def test_200_ok(self, app: TestClient, db: Session, project_data: dict):
        rep_create = app.post("/projects/", json=project_data).json()
        rep_get = app.get(f"/projects/{rep_create['id']}")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_create

    def test_404_not_found(self, app: TestClient, db: Session):
        project_id = 1
        msg = f"Project with ID {project_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get(f"/projects/{project_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-project"])
class TestGetProjects:
    def test_200_ok(self, app: TestClient, db: Session, project_data: dict):
        project_data_1 = {
            "label": "Project Alpha",
            "description": "Description of Project Alpha",
            "creator_id": project_data["creator_id"],
        }
        rep_create_1 = app.post("/projects/", json=project_data).json()
        rep_create_2 = app.post("/projects/", json=project_data_1).json()

        rep_get = app.get("/projects/")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == [rep_create_1, rep_create_2]

    def test_404_not_found(self, app: TestClient, db: Session):
        msg = "No projects found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get("/projects/")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-project"])
class TestUpdateProject:
    def test_200_ok_non_empty_data(
        self, app: TestClient, db: Session, project_data: dict
    ):
        rep_post = app.post("/projects/", json=project_data).json()

        new_data = {"label": "Project Gamma", "description": "Updated description"}
        rep_put = app.put(f"/projects/{rep_post['id']}", json=new_data)

        assert rep_put.status_code == status.HTTP_200_OK
        assert rep_put.json()["label"] == new_data["label"]
        assert rep_put.json()["description"] == new_data["description"]

    def test_200_ok_empty_data(self, app: TestClient, db: Session, project_data: dict):
        rep_post = app.post("/projects/", json=project_data).json()
        rep_get = app.put(f"/projects/{rep_post['id']}", json={})

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post

    def test_404_not_found(self, app: TestClient, db: Session):
        project_id = 1
        new_data = {"label": "Project Gamma", "description": "Updated description"}
        msg = f"Project with ID {project_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.put(f"/projects/{project_id}", json=new_data)
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-project"])
class TestDeleteProject:
    def test_200_ok(self, app: TestClient, db: Session, project_data: dict):
        rep_post = app.post("/projects/", json=project_data).json()
        rep_delete = app.delete(f"/projects/{rep_post['id']}")

        assert rep_delete.status_code == status.HTTP_200_OK

    def test_404_not_found(self, app: TestClient, db: Session):
        project_id = 1
        msg = f"Project with ID {project_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.delete(f"/projects/{project_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg
