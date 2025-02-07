from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Params
from fastapi import APIRouter, Request, status
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select

from src.models import Comment
from src.backend.config import LOG_APP
from src.routers.utils import raise_not_found_if_absent
from src.schemas import CommentCreate, CommentRead, CommentUpdate

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create(request: Request, data: CommentCreate) -> CommentRead:
    LOG_APP.info("Attempting to create a comment")
    db: Session = request.state.db

    comment = Comment(
        content=data.content,
        creator_id=data.creator_id,
        ticket_id=data.ticket_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    comment_read = CommentRead.model_validate(comment)
    LOG_APP.info(f"Comment created successfully: {comment_read.id}")
    return comment_read


@router.get("/{id}", response_model=CommentRead)
async def get(request: Request, id: int) -> CommentRead:
    LOG_APP.info(f"Attempting to get a comment: {id}")
    db: Session = request.state.db

    comment = db.query(Comment).filter(Comment.id == id).first()
    raise_not_found_if_absent(comment, f"Comment with ID {id} not found")

    comment_read = CommentRead.model_validate(comment)
    LOG_APP.info(f"Comment retrieved successfully: {comment_read.id}")
    return comment_read


# GET /comments/?page=1&size=10
@router.get("/", response_model=Page[CommentRead])
async def get_all(request: Request, params: Params = Depends()) -> Page[CommentRead]:
    LOG_APP.info("Attempting to get comments with pagination")
    db: Session = request.state.db

    comments = paginate(db, select(Comment))

    raise_not_found_if_absent(comments.items, "No comments found")

    comments_read = [CommentRead.model_validate(comment) for comment in comments.items]
    LOG_APP.info(
        f"Retrieved {len(comments_read)} comments from the database with pagination."
    )

    return Page[CommentRead].create(
        items=comments_read, params=comments.params, total=comments.total
    )


@router.put("/{id}", response_model=CommentRead)
async def update(request: Request, id: int, data: CommentUpdate) -> CommentRead:
    LOG_APP.info(f"Attempting to update a comment: {id}")
    db: Session = request.state.db
    comment = db.query(Comment).filter(Comment.id == id).first()

    raise_not_found_if_absent(comment, f"Comment with ID {id} not found")

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        LOG_APP.info(f"No update data provided for comment: {id}")
        return CommentRead.model_validate(comment)

    for key, value in update_data.items():
        setattr(comment, key, value)

    db.commit()
    db.refresh(comment)

    comment_read = CommentRead.model_validate(comment)
    LOG_APP.info(f"Comment updated successfully: {comment_read.id}")
    return comment_read


@router.delete("/{id}")
async def delete(request: Request, id: int) -> None:
    LOG_APP.info(f"Attempting to delete a comment: {id}")
    db: Session = request.state.db
    comment = db.query(Comment).filter(Comment.id == id).first()

    raise_not_found_if_absent(comment, f"Comment with ID {id} not found")

    db.delete(comment)
    db.commit()
    LOG_APP.info(f"Comment with ID {id} deleted successfully")
