from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    label: str = Field(..., max_length=20)


class CategoryCreate(CategoryBase): ...


class CategoryRead(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdate(BaseModel):
    label: str | None = Field(None, max_length=20)
