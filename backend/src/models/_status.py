from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from src.models._base import Base


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    label: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
