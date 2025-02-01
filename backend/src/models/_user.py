from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from src.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    tickets: Mapped[list[Ticket]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    comments: Mapped[list[Comment]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"User("
            f"id={self.id!r}, "
            f"nom={self.name!r}, "
            f"email={self.email!r}, "
            f"role={self.role!r}"
            f")"
        )
