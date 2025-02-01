from typing import Optional

from fastapi import APIRouter, Request
from sqlalchemy.exc import IntegrityError

from src.models import Level
from src.schemas._level import LevelCreate, LevelRead

from src.backend.config import LOG_APP

router = APIRouter()


@router.post("/levels/", response_model=LevelRead)
async def create_level(request: Request, data: LevelCreate) -> LevelRead:
    LOG_APP.info(f"Attempting to create a level: {data.name}")
    db = request.state.db
    level = Level(name=data.name)
    db.add(level)
    db.commit()
    db.refresh(level)
    level_read = LevelRead.model_validate(level)
    LOG_APP.info(f"Level created successfully: {level_read.id} - {level_read.name}")
    return level_read


@router.get("/levels/{level_id}", response_model=Optional[LevelRead])
async def get_level(request: Request, level_id: int) -> Optional[LevelRead]:
    db = request.state.db
    level = db.query(Level).filter(Level.id == level_id).first()
    return LevelRead.model_validate(level) if level else None


@router.get("/levels/", response_model=list[LevelRead])
async def get_levels(request: Request) -> list[LevelRead]:
    db = request.state.db
    levels = db.query(Level).all()
    return [LevelRead.model_validate(level) for level in levels]


@router.put("/levels/{level_id}", response_model=Optional[LevelRead])
async def update_level(
    request: Request, level_id: int, level_data: LevelCreate
) -> Optional[LevelRead]:
    db = request.state.db
    level = db.query(Level).filter(Level.id == level_id).first()
    if level:
        level.name = level_data.name
        try:
            db.commit()
            db.refresh(level)
            return LevelRead.model_validate(level)
        except IntegrityError:
            db.rollback()
    return None


@router.delete("/levels/{level_id}", response_model=bool)
async def delete_level(request: Request, level_id: int) -> bool:
    db = request.state.db
    level = db.query(Level).filter(Level.id == level_id).first()
    if level:
        db.delete(level)
        db.commit()
        return True
    return False
