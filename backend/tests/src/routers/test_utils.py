# def test_invalid_credentials(self, app: TestClient, db: Session, user_data: dict):
#     # msg = "Incorrect username or password"
#     username = "invaliduser"
#     msg = f"User '{username}' not found"
#     with pytest.raises(CredentialsException, match=msg):
#         response = app.post(
#             "/auth/login",
#             data={"username": username, "password": "invalidpassword"},
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.json()["detail"] == msg


# def test_invalid_credentials(self, app: TestClient, db: Session, user_data: dict):
#     msg = "User not found"
#     with pytest.raises(CredentialsException, match=msg):
#         response = app.post(
#             "/auth/forgot-password",
#             json={"email": "nonexistent@example.com"},
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.json()["detail"] == msg


# def test_invalid_token(self, app: TestClient, db: Session):
#     msg = "Invalid token"
#     with pytest.raises(CredentialsException, match=msg):
#         token = "invalid token"
#         headers = {"Authorization": f"Bearer {token}"}
#         response = app.post(
#             "/auth/reset-password",
#             headers=headers,
#             json={"password": "new password"},
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.json()["detail"] == "Invalid token"

# @staticmethod
# def create_expired_token(username: str):
#     expire = datetime.now(timezone.utc) - timedelta(minutes=1)
#     to_encode = {"sub": username, "exp": expire}
#     return jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)

# def test_expired_token(self, app: TestClient, db: Session, user_data: dict):
#     msg = "Token has expired"
#     with pytest.raises(CredentialsException, match=msg):
#         token = self.create_expired_token(user_data["username"])
#         headers = {"Authorization": f"Bearer {token}"}
#         response = app.post(
#             "/auth/reset-password",
#             headers=headers,
#             json={"password": "new password"},
#         )

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.json()["detail"] == msg

# def test_sub_token_missing(self, app: TestClient, db: Session, user_data: dict):
#     msg = "Invalid token"
#     with pytest.raises(CredentialsException, match=msg):
#         token = jwt.encode(
#             {"exp": datetime.now(timezone.utc) + timedelta(minutes=1)},
#             SECRET_KEY,
#             algorithm=ALGORITHM,
#         )
#         headers = {"Authorization": f"Bearer {token}"}
#         response = app.post(
#             "/auth/reset-password",
#             headers=headers,
#             json={"password": "new password"},
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.json()["detail"] == msg

# def test_user_not_found(self, app: TestClient, db: Session, user_data: dict):
#     msg = f"User '{user_data['username']}' not found"

#     with pytest.raises(CredentialsException, match=msg):
#         token = jwt.encode(
#             {
#                 "sub": user_data["username"],
#                 "exp": datetime.now(timezone.utc) + timedelta(minutes=1),
#             },
#             SECRET_KEY,
#             algorithm=ALGORITHM,
#         )
#         headers = {"Authorization": f"Bearer {token}"}
#         response = app.post(
#             "/auth/reset-password",
#             headers=headers,
#             json={"password": "new password"},
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.json()["detail"] == msg


class TestGetCurrentUser:
    def test_get_current_user(self, app: TestClient, db: Session, user_data: dict):
        data = user_data
        rep = app.post("/users/", json=data).json()

        response = app.post(
            "/auth/login",
            data={"username": user_data["username"], "password": user_data["password"]},
        )
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}

        # Tester la suppression du compte
        response = app.get("/auth/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == rep


import smtplib
from unittest.mock import patch


def send_email(subject, body, to_email):
    # Configuration du serveur SMTP
    smtp_server = "smtp.example.com"
    smtp_port = 587
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    # Création du message
    message = f"Subject: {subject}\n\n{body}"

    # Connexion au serveur SMTP et envoi de l'email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message)


# Test avec unittest.mock
@patch("smtplib.SMTP")
def test_send_email(mock_smtp):
    # Configuration du mock
    mock_server = mock_smtp.return_value
    mock_server.starttls.return_value = True
    mock_server.login.return_value = True
    mock_server.sendmail.return_value = {}

    # Appel de la fonction à tester
    send_email("Test Subject", "Test Body", "recipient@example.com")

    # Vérifications
    mock_smtp.assert_called_once_with("smtp.example.com", 587)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("your_email@example.com", "your_password")
    mock_server.sendmail.assert_called_once_with(
        "your_email@example.com",
        "recipient@example.com",
        "Subject: Test Subject\n\nTest Body",
    )


# Exécution du test
if __name__ == "__main__":
    test_send_email()
    print("Test réussi !")
