from fastapi import APIRouter, Request, status, Depends
from fastapi_pagination import Params
from fastapi_pagination.links.default import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from src.routers.pagination import PageResponse
from sqlalchemy.future import select

from src.models import User
from src.backend.config import LOG_APP

from src.routers.utils import raise_not_found_if_absent
from src.schemas._user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create(request: Request, data: UserCreate) -> UserRead:
    LOG_APP.info(f"Attempting to create a user {data.username}")
    db = request.state.db

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        email=data.email,
        role=data.role,
        plain_password=data.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_read = UserRead.model_validate(user)
    LOG_APP.info(f"Comment created successfully: {user_read.id} - {user_read.username}")
    return user_read


@router.get("/{id}", response_model=UserRead)
async def get(request: Request, id: int) -> UserRead:
    LOG_APP.info(f"Attempting to get a user: {id}")
    db = request.state.db
    user = db.query(User).filter(User.id == id).first()
    raise_not_found_if_absent(user, f"User with ID {id} not found")

    user_read = UserRead.model_validate(user)
    LOG_APP.info(f"User retrieved successfully: {user_read.id} - {user_read.username}")
    return user_read


@router.get("/", response_model=Page[UserRead])
async def get_all(request: Request, params: Params = Depends()) -> Page[UserRead]:
    LOG_APP.info("Attempting to get users with pagination")
    db = request.state.db

    users = await paginate(db, select(User), params)

    raise_not_found_if_absent(users.items, "No users found")

    users_read = [UserRead.model_validate(user) for user in users.items]
    LOG_APP.info(
        f"Retrieved {len(users_read)} users from the database with pagination."
    )

    return Page[UserRead].create(users_read, params, total=users.total)


@router.put("/{id}", response_model=UserRead)
async def update(request: Request, id: int, data: UserUpdate) -> UserRead:
    LOG_APP.info(f"Attempting to update a user: {id}")
    db = request.state.db
    user = db.query(User).filter(User.id == id).first()

    raise_not_found_if_absent(user, f"User with ID {id} not found")

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        LOG_APP.info(f"No update data provided for user: {id}")
        return UserRead.model_validate(user)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    user_read = UserRead.model_validate(user)
    LOG_APP.info(f"User updated successfully: {user_read.id} - {user_read.username}")
    return user_read


@router.delete("/{id}")
async def delete(request: Request, id: int) -> None:
    LOG_APP.info(f"Attempting to delete a user: {id}")
    db = request.state.db
    user = db.query(User).filter(User.id == id).first()

    raise_not_found_if_absent(user, f"User with ID {id} not found")

    db.delete(user)
    db.commit()
    LOG_APP.info(f"User with ID {id} deleted successfully")
