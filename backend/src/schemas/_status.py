from pydantic import BaseModel, ConfigDict, Field


class StatusBase(BaseModel):
    label: str = Field(..., max_length=20)


class StatusCreate(StatusBase): ...


class StatusRead(StatusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StatusUpdate(BaseModel):
    label: str | None = Field(None, max_length=20)
