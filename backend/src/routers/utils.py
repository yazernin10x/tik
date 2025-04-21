from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart


from sqlalchemy.orm import Session
from jose import ExpiredSignatureError, JWTError, jwt
from fastapi import Depends

from src.models import User
from src.exceptions import CredentialsException
from src.exceptions import NotFoundException
from schemas._auth import TokenData
from src.backend.config import (
    LOG_APP,
    ALGORITHM,
    SECRET_KEY,
    OAUTH2_SCHEME,
    SESSION_LOCAL,
)


def raise_not_found_if_absent(item: object, message: str):
    """
    Raise a NotFoundException if the item is None.

    Parameters
    ----------
    item : object
        The item to check for absence.

    message : str
        The message to raise if the item is None.
    """
    if not item:
        LOG_APP.warning(message)
        raise NotFoundException(message)


def get_db():
    """
    Get a database session.

    Returns
    -------
    db : Session
    """
    db = SESSION_LOCAL()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def send_email(from_address: str, to_address: str, subject: str, body: str) -> None:
    """
    Send an email.

    Parameters
    ----------
    from_address : str
        The address of the sender.

    to_address : str
        The address of the recipient.

    subject : str
        The subject of the email.

    body : str
        The body of the email.
    """
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(body))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("yazernin10x@gmail.com", "joxf cdmd dgym euzb")

        server.sendmail(from_address, to_address, msg.as_string())
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

    finally:
        server.quit()


def get_user(db: Session, **filters) -> User:
    """
    Get a user from the database.

    Parameters
    ----------
    db : Session
        The database session.

    **filters : dict
        The filters to apply to the query.

    Returns
    -------
    user : User
    """
    if not filters:
        raise ValueError("At least one filter must be provided")

    query = db.query(User)
    for attr, value in filters.items():
        query = query.filter(getattr(User, attr) == value)

    user = query.first()
    if user is None:
        # filter_str = ", ".join(f"{k}='{v}'" for k, v in filters.items())
        raise CredentialsException("User not found")

    return user


def decode_token(token: str) -> dict:
    """Decode a token.

    Parameters
    ----------
    token : str
        The token to decode.

    Returns
    -------
    payload : dict
        The payload of the token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError as e:

        raise CredentialsException("Token has expired") from e
    except JWTError as e:
        raise CredentialsException("Invalid token") from e
    return payload


def get_token_data(token: str) -> TokenData:
    """
    Get the token data from a token.

    Parameters
    ----------
    token : str
        The token to get the data from.

    Returns
    -------
    token_data : TokenData
        The token data.
    """
    payload = decode_token(token)
    username: str | None = payload.get("sub")
    if username is None:

        raise CredentialsException("Invalid token")
    return TokenData(username=username)


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
):
    """
    Get the current user.

    Parameters
    ----------
    token : str
        The token to get the current user from.

    db : Session
        The database session.

    Returns
    -------
    user : User
    """
    token_data = get_token_data(token)
    user = get_user(db, username=token_data.username)
    return user
