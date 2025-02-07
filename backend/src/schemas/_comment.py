from __future__ import annotations
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    content: str = Field(..., max_length=500)


class CommentCreate(CommentBase):
    creator_id: int
    ticket_id: int


class CommentReadLight(CommentBase):
    id: int
    creation_date: date
    update_date: date | None = None
    model_config = ConfigDict(from_attributes=True)


class CommentRead(CommentReadLight):
    creator: UserReadLight
    ticket: TicketReadLight

    model_config = ConfigDict(from_attributes=True)


class CommentUpdate(BaseModel):
    content: str | None = Field(None, max_length=500)
