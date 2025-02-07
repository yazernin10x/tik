from typing import Annotated
from fastapi import APIRouter, Body, Path, Query, Request, status


from src.models import Category
from src.backend.config import LOG_APP
from src.routers.utils import raise_not_found_if_absent
from src.schemas import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create(
    request: Request, data: Annotated[CategoryCreate, Body()]
) -> CategoryRead:
    LOG_APP.info(f"Attempting to create a category: {data.label}")
    db = request.state.db
    category = Category(label=data.label)

    db.add(category)
    db.commit()
    db.refresh(category)
    category_read = CategoryRead.model_validate(category)
    LOG_APP.info(
        f"Category created successfully: {category_read.id} - {category_read.label}"
    )
    return category_read


@router.get("/{id}", response_model=CategoryRead)
async def get(request: Request, id: Annotated[int, Path()]) -> CategoryRead:
    LOG_APP.info(f"Attempting to get a category: {id}")
    db = request.state.db
    category = db.query(Category).filter(Category.id == id).first()

    raise_not_found_if_absent(category, f"Category with ID {id} not found")

    category_read = CategoryRead.model_validate(category)
    LOG_APP.info(
        f"Category retrieved successfully: {category_read.id} - {category_read.label}"
    )
    return category_read


@router.get("/", response_model=list[CategoryRead])
async def get_all(request: Request) -> list[CategoryRead]:
    LOG_APP.info("Attempting to get all categories")
    db = request.state.db
    categories = db.query(Category).all()

    raise_not_found_if_absent(categories, "No categories found")

    categories_read = [CategoryRead.model_validate(category) for category in categories]
    LOG_APP.info(f"Retrieved {len(categories_read)} categories from the database.")
    return categories_read


@router.put("/{id}", response_model=CategoryRead)
async def update(
    request: Request,
    id: Annotated[int, Path(ge=0)],
    data: Annotated[CategoryUpdate, Body()],
) -> CategoryRead:
    LOG_APP.info(f"Attempting to update a category: {id}")
    db = request.state.db
    category = db.query(Category).filter(Category.id == id).first()

    raise_not_found_if_absent(category, f"Category with ID {id} not found")

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        LOG_APP.info(f"No update data provided for category: {id}")
        return CategoryRead.model_validate(category)

    category.label = data.label
    db.commit()
    db.refresh(category)

    category_read = CategoryRead.model_validate(category)
    LOG_APP.info(
        f"Category updated  successfully: {category_read.id} - {category_read.label}"
    )
    return category_read


@router.delete("/{id}", response_model=CategoryRead)
async def delete(
    request: Request,
    id: Annotated[int, Path()],
) -> CategoryRead:
    LOG_APP.info(f"Attempting to delete a category: {id}")
    db = request.state.db
    category = db.query(Category).filter(Category.id == id).first()

    raise_not_found_if_absent(category, f"Category with ID {id} not found")

    db.delete(category)
    db.commit()

    LOG_APP.info(f"Category with ID {id} deleted successfully")
    return category
