from fastapi import APIRouter, Request, status

from src.models import Level
from src.backend.config import LOG_APP
from src.exceptions import NotFoundException
from src.routers.utils import raise_not_found_if_absent
from src.schemas import LevelCreate, LevelRead, LevelUpdate


router = APIRouter(prefix="/levels", tags=["Levels"])


@router.post("/", response_model=LevelRead, status_code=status.HTTP_201_CREATED)
async def create(request: Request, data: LevelCreate) -> LevelRead:
    LOG_APP.info(f"Attempting to create a level: {data.label}")
    db = request.state.db

    level = Level(label=data.label)
    db.add(level)
    db.commit()
    db.refresh(level)

    level_read = LevelRead.model_validate(level)
    LOG_APP.info(f"Level created successfully: {level_read.id} - {level_read.label}")
    return level_read


@router.get("/{id}", response_model=LevelRead)
async def get(request: Request, id: int) -> LevelRead:
    LOG_APP.info(f"Attempting to get a level: {id}")
    db = request.state.db
    level = db.query(Level).filter(Level.id == id).first()

    raise_not_found_if_absent(level, f"Level with ID {id} not found")

    level_read = LevelRead.model_validate(level)
    LOG_APP.info(f"Level retrieved successfully: {level_read.id} - {level_read.label}")
    return level_read


@router.get("/", response_model=list[LevelRead])
async def get_all(request: Request) -> list[LevelRead]:
    LOG_APP.info("Attempting to get all levels")
    db = request.state.db
    levels = db.query(Level).all()

    if not levels:
        LOG_APP.warning("No levels found in the database.")
        raise NotFoundException("No levels found")

    raise_not_found_if_absent(levels, "No levels found")

    levels_read = [LevelRead.model_validate(level) for level in levels]
    LOG_APP.info(f"Retrieved {len(levels_read)} levels from the database.")
    return levels_read


@router.put("/{id}", response_model=LevelRead)
async def update(request: Request, id: int, data: LevelUpdate) -> LevelRead:
    LOG_APP.info(f"Attempting to update a level: {id}")
    db = request.state.db
    level = db.query(Level).filter(Level.id == id).first()

    raise_not_found_if_absent(level, f"Level with ID {id} not found")

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        LOG_APP.info(f"No update data provided for level: {id}")
        return LevelRead.model_validate(level)

    level.label = data.label
    db.commit()
    db.refresh(level)

    level_read = LevelRead.model_validate(level)
    LOG_APP.info(f"Level updated  successfully: {level_read.id} - {level_read.label}")
    return level_read


@router.delete("/{id}")
async def delete(request: Request, id: int) -> None:
    LOG_APP.info(f"Attempting to delete a level: {id}")
    db = request.state.db
    level = db.query(Level).filter(Level.id == id).first()

    raise_not_found_if_absent(level, f"Level with ID {id} not found")

    db.delete(level)
    db.commit()

    LOG_APP.info(f"Level with ID {id} deleted successfully")
