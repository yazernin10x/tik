from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Date, func

from src.models import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    comments: Mapped[list[Comment]] = relationship(
        back_populates="ticket",
        cascade="all, delete-orphan",
        init=False,
    )

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    creator: Mapped[User] = relationship(back_populates="tickets", init=False)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped[Project] = relationship(back_populates="tickets", init=False)

    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    status: Mapped[Status] = relationship(init=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    category: Mapped[Category] = relationship(init=False)

    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"), nullable=False)
    level: Mapped[Level] = relationship(init=False)

    creation_date: Mapped[Date] = mapped_column(
        Date, nullable=False, insert_default=func.current_date(), init=False
    )

    update_date: Mapped[Date | None] = mapped_column(
        Date, insert_default=None, onupdate=func.current_date(), init=False
    )
