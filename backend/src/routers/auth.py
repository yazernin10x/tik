from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Body, Request, Depends, Query

from src.schemas import UserRead, ForgotPasswordRequest, PasswordResetRequest, Token
from src.models import User, RevokedToken
from src.exceptions import CredentialsException
from src.backend.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    LOG_APP,
    OAUTH2_SCHEME,
    SECRET_KEY,
)
from src.routers.utils import (
    decode_token,
    get_current_user,
    get_db,
    get_token_data,
    get_user,
    send_email,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user by username and password.

    Parameters
    ----------
    db : Session
        Database session.
    username : str
        Username of the user.
    password : str
        Password of the user.

    Returns
    -------
    User
        User object.

    Raises
    ------
    CredentialsException
        If the username or password is incorrect.
    """
    try:
        user = get_user(db, username=username)

        if not user.verify_password(password):
            raise CredentialsException
    except CredentialsException:
        raise CredentialsException("Incorrect username or password")

    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    """Create an access token for a user.

    Parameters
    ----------
    data : dict
        Data to encode in the token, must contain a "sub" key with the username.
    expires_delta : timedelta, optional
        Time before the token expires, by default ACCESS_TOKEN_EXPIRE_MINUTES minutes.

    Returns
    -------
    str
        Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def verify_token(token: str, db: Session):
    """Verify token is valid and not revoked.

    Parameters
    ----------
    token : str
        The token to verify.
    db : Session
        The database session.
    """
    if db.query(RevokedToken).filter(RevokedToken.token == token).first():
        raise CredentialsException("Token has been revoked")
    decode_token(token)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    LOG_APP.info(f"Login attempt for user: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    LOG_APP.info(f"Login successful for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)):
    LOG_APP.info(f"Logout attempt for token: {token}")
    verify_token(token, db)
    db_token = RevokedToken(token=token)
    db.add(db_token)
    db.commit()
    LOG_APP.info(f"Logout successful for token: {token}")
    return {"message": "Successfully logged out"}


@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    data: ForgotPasswordRequest = Body(...),
    db: Session = Depends(get_db),
):
    LOG_APP.info(f"Forgot password attempt for email: {data.email}")
    user = get_user(db, email=data.email)
    reset_token = create_access_token(data={"sub": user.username})
    send_email(
        "yazernin10x@gmail.com",
        user.email,
        "Password Reset",
        (
            f"Use this token to reset your password: "
            f"{request.base_url}auth/reset-password?token={reset_token}"
        ),
    )
    LOG_APP.info(f"Password reset email sent for email: {data.email}")
    return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(
    data: PasswordResetRequest = Body(...),
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    LOG_APP.info(f"Reset password attempt for token: {token}")
    token_data = get_token_data(token)
    user = get_user(db, username=token_data.username)
    user.set_password(data.password)
    db.commit()
    LOG_APP.info(f"Password updated successfully for token: {token}")
    return {"message": "Password updated successfully"}


@router.delete("/account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    LOG_APP.info(f"Delete account attempt for user: {current_user.username}")
    db.delete(current_user)
    db.commit()
    LOG_APP.info(f"Account deleted successfully for user: {current_user.username}")
    return {"message": "Account deleted successfully"}


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    LOG_APP.info(f"Read user me attempt for user: {current_user.username}")
    return current_user
