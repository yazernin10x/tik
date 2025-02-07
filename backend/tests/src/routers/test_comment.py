import pytest
from fastapi import status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import Comment
from src.exceptions import NotFoundException


@pytest.mark.dependency(name="create-comment")
class TestCreateComment:
    def test_201_created(
        self, app: TestClient, db: Session, comment_data: dict
    ) -> None:
        data = comment_data
        rep = app.post("/comments/", json=data)

        assert rep.status_code == status.HTTP_201_CREATED

        rep_data = rep.json()
        assert rep_data["content"] == data["content"]
        assert rep_data["creator"]["id"] == data["creator_id"]
        assert rep_data["ticket"]["id"] == data["ticket_id"]
        assert "id" in rep_data

        comment = db.query(Comment).filter(Comment.id == rep_data["id"]).first()
        assert comment is not None
        assert comment.content == data["content"]
        assert comment.creator.id == data["creator_id"]
        assert comment.ticket.id == data["ticket_id"]


@pytest.mark.dependency(depends=["create-comment"])
class TestGetComment:
    def test_200_ok(self, app: TestClient, db: Session, comment_data: dict):
        rep_create = app.post("/comments/", json=comment_data).json()
        rep_get = app.get(f"/comments/{rep_create['id']}")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_create

    def test_404_not_found(self, app: TestClient, db: Session):
        comment_id = 1
        msg = f"Comment with ID {comment_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get(f"/comments/{comment_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-comment"])
class TestGetAllComments:
    def test_200_ok(self, app: TestClient, db: Session, comment_data):
        comment_data_1 = {
            "content": "This is comment 2",
            "creator_id": comment_data["creator_id"],
            "ticket_id": comment_data["ticket_id"],
        }

        rep_create_1 = app.post("/comments/", json=comment_data).json()
        rep_create_2 = app.post("/comments/", json=comment_data_1).json()

        rep_get = app.get("/comments/")
        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == [rep_create_1, rep_create_2]

    def test_404_not_found(self, app: TestClient, db: Session):
        msg = "No comments found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.get("/comments/")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-comment"])
class TestUpdateComment:
    def test_200_ok_non_empty_data(self, app: TestClient, db: Session, comment_data):
        rep_post = app.post("/comments/", json=comment_data).json()

        new_data = {"content": "Updated comment"}
        rep_put = app.put(f"/comments/{rep_post['id']}", json=new_data)

        assert rep_put.status_code == status.HTTP_200_OK
        assert rep_put.json()["content"] == new_data["content"]

    def test_200_ok_empty_data(self, app: TestClient, db: Session, comment_data):
        rep_post = app.post("/comments/", json=comment_data).json()
        rep_get = app.put(f"/comments/{rep_post['id']}", json={})

        assert rep_get.status_code == status.HTTP_200_OK
        assert rep_get.json() == rep_post

    def test_404_not_found(self, app: TestClient, db: Session):
        comment_id = 1
        new_data = {"content": "Updated comment"}
        msg = f"Comment with ID {comment_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.put(f"/comments/{comment_id}", json=new_data)
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg


@pytest.mark.dependency(depends=["create-comment"])
class TestDeleteComment:
    def test_200_ok(self, app: TestClient, db: Session, comment_data):
        rep_post = app.post("/comments/", json=comment_data).json()
        rep_delete = app.delete(f"/comments/{rep_post['id']}")

        assert rep_delete.status_code == status.HTTP_200_OK

    def test_404_not_found(self, app: TestClient, db: Session):
        comment_id = 1
        msg = f"Comment with ID {comment_id} not found"
        with pytest.raises(NotFoundException, match=msg) as excinfo:
            rep = app.delete(f"/comments/{comment_id}")
            assert rep.status_code == status.HTTP_404_NOT_FOUND

        assert str(excinfo.value).split(": ")[1] == msg
