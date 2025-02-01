from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from src.models import Base


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Level(id={self.id!r}, name={self.name!r})"
