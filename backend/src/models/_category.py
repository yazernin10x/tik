from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    label: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
