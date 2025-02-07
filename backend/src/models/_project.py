from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Date, func

from src.models import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    creator: Mapped[User] = relationship(back_populates="projects", init=False)

    tickets: Mapped[list[Ticket]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        init=False,
    )

    creation_date: Mapped[Date] = mapped_column(
        Date, nullable=False, insert_default=func.current_date(), init=False
    )
    update_date: Mapped[Date | None] = mapped_column(
        Date, insert_default=None, onupdate=func.current_date(), init=False
    )
