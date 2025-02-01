from __future__ import annotations
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date
from datetime import date

from src.models import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    creation_date: Mapped[date] = mapped_column(
        Date, nullable=False, default=date.today
    )
    update_date: Mapped[Optional[date]] = mapped_column(Date, onupdate=date.today)

    tickets: Mapped[list[Ticket]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Project("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"creation_date={self.creation_date!r}"
            f")"
        )
