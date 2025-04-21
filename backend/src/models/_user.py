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
        "password", String(255), nullable=False, init=False, repr=False
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

    password: InitVar[str] = None

    def __post_init__(self, password: str):
        self.set_password(password)

    def set_password(self, password: str):
        """Hash and store the password.

        Parameters
        ----------
        password_ : str
            The  text password to be hashed and stored.
        """
        salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode("utf-8"), salt)

    def verify_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash.

        Parameters
        ----------
        _password : str
            The  text password to be verified.

        Returns
        -------
        bool
            True if the provided password matches the stored hash, False otherwise.
        """
        if self._password is None:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self._password)
