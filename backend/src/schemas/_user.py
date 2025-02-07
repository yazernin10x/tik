from __future__ import annotations
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    username: str = Field(..., max_length=50)
    email: EmailStr
    role: str = Field(..., max_length=20)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserReadLight(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserReadLight):
    tickets: Optional[list[TicketRead]] = None
    comments: Optional[list[CommentRead]] = None
    projects: Optional[list[ProjectRead]] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=50)
    last_name: str | None = Field(None, max_length=50)
    username: str | None = Field(None, max_length=50)
    email: EmailStr | None = None
    role: str | None = Field(None, max_length=20)
    password: str | None = Field(None, min_length=8)
