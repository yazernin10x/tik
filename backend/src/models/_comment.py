from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey, func

from src.models import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    creator: Mapped[User] = relationship(back_populates="comments", init=False)

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    ticket: Mapped[Ticket] = relationship(back_populates="comments", init=False)

    creation_date: Mapped[Date] = mapped_column(
        Date, nullable=False, insert_default=func.current_date(), init=False
    )

    update_date: Mapped[Date | None] = mapped_column(
        Date, insert_default=None, onupdate=func.current_date(), init=False
    )
