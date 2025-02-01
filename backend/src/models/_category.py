from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"
