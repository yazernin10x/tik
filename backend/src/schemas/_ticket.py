from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TicketBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)


class TicketCreate(TicketBase):
    creator_id: int
    project_id: int
    status_id: int
    category_id: int
    level_id: int


class TicketReadLight(TicketBase):
    id: int
    creation_date: date
    status: StatusRead
    level: LevelRead
    category: CategoryRead
    update_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class TicketRead(TicketReadLight):
    creator: UserReadLight
    project: ProjectReadLight
    comments: Optional[list[CommentReadLight]] = None

    model_config = ConfigDict(from_attributes=True)


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status_id: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
