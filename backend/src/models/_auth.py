from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"
    token: Mapped[str] = mapped_column(String, primary_key=True)
