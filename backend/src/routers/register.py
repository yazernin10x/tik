from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
import smtplib

from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from src.models import User
from src.schemas import UserCreate
from src.schemas.token import TokenData
from src.exceptions import CredentialsException
from src.backend.config import ALGORITHM, OAUTH2_SCHEME, SECRET_KEY, SessionLocal

router = APIRouter(prefix="/register", tags=["Register"])


def get_user(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    return user if user and user.verify_password(password) else None


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def send_reset_password_email(email: str, token: str):
    msg = MIMEText(f"Use this token to reset your password: {token}")
    # msg["Subject"] = "Password Reset"
    # msg["From"] = "noreply@gmail.com"
    # msg["To"] = email

    # with smtplib.SMTP("smtp.yourapp.com") as server:
    #     server.send_message(msg)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except JWTError | ExpiredSignatureError:
        raise CredentialsException

    user = get_user(db, username=token_data.username)
    if user is None:
        raise CredentialsException
    return user
