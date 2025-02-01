from __future__ import annotations
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey

from src.models import Base


class Comment(Base):

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    creation_date: Mapped[date] = mapped_column(
        Date, nullable=False, default=date.today
    )

    # ondelete="CASCADE" signifie que si l'utilisateur
    # (dans la table users) associé à ce commentaire est
    # supprimé, tous les commentaires associés à cet utilisateur
    # seront automatiquement supprimés.
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped[User] = relationship(back_populates="comments")

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    ticket: Mapped[Ticket] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return (
            f"Comment("
            f"id={self.id!r}, "
            f"content={self.content!r}, "
            f"creation_date={self.creation_date!r}, "
            f"user_id={self.user_id!r}"
            f")"
        )
