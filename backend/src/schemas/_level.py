from pydantic import BaseModel, ConfigDict, Field


class LevelBase(BaseModel):
    label: str = Field(..., max_length=20)


class LevelCreate(LevelBase): ...


class LevelRead(LevelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class LevelUpdate(BaseModel):
    label: str | None = Field(None, max_length=20)
