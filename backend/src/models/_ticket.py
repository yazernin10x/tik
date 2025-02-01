from __future__ import annotations
from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Date


from src.models import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    creation_date: Mapped[date] = mapped_column(
        Date, nullable=False, default=date.today
    )

    update_date: Mapped[Optional[date]] = mapped_column(Date, onupdate=date.today)

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(back_populates="tickets")

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped[Project] = relationship(back_populates="tickets")

    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    status: Mapped[Status] = relationship()

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    category: Mapped[Category] = relationship()

    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"), nullable=False)
    level: Mapped[Level] = relationship()

    def __repr__(self) -> str:
        return (
            f"Ticket("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"description={self.description!r}, "
            f"user_id={self.user_id!r}, "
            f"status_id={self.status_id!r}, "
            f"category_id={self.category_id!r}, "
            f"level_id={self.level_id!r}, "
            f"creation_date={self.creation_date!r}, "
            f"update_date={self.update_date!r}"
            f")"
        )
