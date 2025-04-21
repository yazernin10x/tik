from typing import Any
import pytest
from fastapi import status

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.models import RevokedToken, User
from src.exceptions import CredentialsException
from src.routers.auth import authenticate_user, create_access_token, verify_token
from tests.conftest import USER_EMAIL, USER_PASSWORD, USER_NAME


class TestAuthenticateUser:
    ERROR_MESSAGE = "Incorrect username or password"

    def test_200_ok(self, db: Session, user: User):
        user = authenticate_user(db, user.username, USER_PASSWORD)
        assert user.username == user.username
        assert user.verify_password(USER_PASSWORD) is True

    def test_401_unauthorized_username_not_found(self, db: Session):
        with pytest.raises(CredentialsException, match=self.ERROR_MESSAGE):
            authenticate_user(db, "nonexistent", USER_PASSWORD)

    def test_401_unauthorized_wrong_password(self, db: Session, user: User):
        with pytest.raises(CredentialsException, match=self.ERROR_MESSAGE):
            authenticate_user(db, user.username, "wrongpassword")


@pytest.mark.dependency(name="create-token")
class TestCreateAccessToken:
    def test_200_ok(self, user: User):
        access_token = create_access_token({"sub": user.username})
        assert access_token is not None


@pytest.mark.dependency(depends=["create-token"])
class TestVerifyToken:
    def test_200_ok(self, db: Session, user: User):
        access_token = create_access_token({"sub": user.username})
        verify_token(access_token, db)

    def test_401_unauthorized(self, db: Session, user: User):
        access_token = create_access_token(data={"sub": user.username})
        db_token = RevokedToken(token=access_token)
        db.add(db_token)
        db.commit()
        with pytest.raises(CredentialsException, match="Token has been revoked"):
            verify_token(access_token, db)


@pytest.mark.dependency(name="login")
class TestLogin:
    def test_201_ok(self, app: TestClient, db: Session, user: User):
        rep = app.post(
            "/auth/login",
            data={"username": user.username, "password": USER_PASSWORD},
        )
        assert rep.status_code == status.HTTP_200_OK
        assert "access_token" in rep.json()
        assert rep.json()["token_type"] == "bearer"


@pytest.mark.dependency(depends=["login"])
class TestLogout:
    def test_logout(self, app: TestClient, db: Session, user_session: dict[str, Any]):
        response = app.post("/auth/logout", headers=user_session["headers"])
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Successfully logged out"}

        query = db.query(RevokedToken)
        db_token = query.filter(RevokedToken.token == user_session["token"]).first()
        assert db_token is not None


class TestForgotPassword:
    def test_200_ok(self, app: TestClient, db: Session, user: User):
        response = app.post(
            "/auth/forgot-password/",
            json={"email": USER_EMAIL},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Password reset email sent"}


class TestResetPassword:
    def test_reset_password(
        self, app: TestClient, db: Session, user_session: dict[str, Any]
    ):
        new_password = "new password"
        response = app.post(
            "/auth/reset-password",
            params={"token": user_session["token"]},
            json={"password": new_password},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Password updated successfully"}

        user_updated = db.query(User).filter(User.username == USER_NAME).first()
        assert user_updated is not None
        assert user_updated.username == USER_NAME
        assert user_updated.verify_password(new_password) is True


class TestAccountDeletion:
    def test_delete_account(
        self, app: TestClient, db: Session, user_session: dict[str, Any]
    ):
        response = app.delete("/auth/account", headers=user_session["headers"])
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Account deleted successfully"}
