from pydantic import BaseModel


class LevelBase(BaseModel):
    name: str


class LevelCreate(LevelBase):
    pass


class LevelRead(LevelBase):
    id: int

    class Config:
        from_attributes = True
