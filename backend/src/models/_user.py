from __future__ import annotations
from dataclasses import InitVar

import bcrypt
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    _password: Mapped[bytes] = mapped_column(
        "password", String(255), nullable=False, init=False
    )

    tickets: Mapped[list[Ticket]] = relationship(
        "Ticket", back_populates="creator", cascade="all, delete-orphan", init=False
    )

    comments: Mapped[list[Comment]] = relationship(
        "Comment", back_populates="creator", cascade="all, delete-orphan", init=False
    )

    projects: Mapped[list[Project]] = relationship(
        "Project", back_populates="creator", cascade="all, delete-orphan", init=False
    )

    plain_password: InitVar[str] = None

    def __post_init__(self, plain_password: str):
        self._password = self._set_password(plain_password)

    @property
    def password(self) -> bytes:
        return self._password

    @password.setter
    def password(self, plain_password: str):
        self._set_password(plain_password)

    def _set_password(self, plain_password: str):
        """Hash and store the password.

        Parameters
        ----------
        plain_password : str
            The plain text password to be hashed and stored.
        """
        salt = bcrypt.gensalt()
        password: bytes = plain_password.encode("utf-8")
        self._password = bcrypt.hashpw(password, salt)

    def verify_password(self, plain_password: str) -> bool:
        """Check if the provided password matches the stored hash.

        Parameters
        ----------
        plain_password : str
            The plain text password to be verified.

        Returns
        -------
        bool
            True if the provided password matches the stored hash, False otherwise.
        """
        if self._password is None:
            return False
        return bcrypt.checkpw(plain_password.encode("utf-8"), self._password)
