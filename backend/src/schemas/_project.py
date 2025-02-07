from __future__ import annotations
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    label: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)


class ProjectCreate(ProjectBase):
    creator_id: int


class ProjectReadLight(ProjectBase):
    id: int
    creation_date: date
    update_date: date | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectRead(ProjectReadLight):
    creator: UserReadLight
    tickets: Optional[list[TicketReadLight]] = None

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    label: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
