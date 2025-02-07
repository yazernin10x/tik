from fastapi import APIRouter, Request, status

from src.models import Status
from src.routers.utils import raise_not_found_if_absent
from src.backend.config import LOG_APP
from src.schemas import StatusCreate, StatusRead, StatusUpdate

router = APIRouter(prefix="/statuses", tags=["Statuses"])


@router.post("/", response_model=StatusRead, status_code=status.HTTP_201_CREATED)
async def create_status(request: Request, data: StatusCreate) -> StatusRead:
    LOG_APP.info(f"Attempting to create a status: {data.label}")
    db = request.state.db
    status = Status(label=data.label)

    db.add(status)
    db.commit()
    db.refresh(status)

    LOG_APP.info(f"Attempting to create a status: {data.label}")
    status_read = StatusRead.model_validate(status)
    LOG_APP.info(f"Status created successfully: {status_read.id} - {status_read.label}")
    return status_read


@router.get("/{id}", response_model=StatusRead)
async def get_status(request: Request, id: int) -> StatusRead:
    LOG_APP.info(f"Attempting to get a status: {id}")
    db = request.state.db
    status = db.query(Status).filter(Status.id == id).first()

    raise_not_found_if_absent(status, f"Status with ID {id} not found")

    status_read = StatusRead.model_validate(status)
    LOG_APP.info(
        f"Status retrieved successfully: {status_read.id} - {status_read.label}"
    )
    return status_read


@router.get("/", response_model=list[StatusRead])
async def get_statuses(request: Request) -> list[StatusRead]:
    LOG_APP.info("Attempting to get all statuses")
    db = request.state.db
    statuses = db.query(Status).all()

    raise_not_found_if_absent(statuses, "No statuses found")

    statuses_read = [StatusRead.model_validate(status) for status in statuses]
    LOG_APP.info(f"Retrieved {len(statuses_read)} statuses from the database.")
    return statuses_read


@router.put("/{id}", response_model=StatusRead)
async def update_status(request: Request, id: int, data: StatusUpdate) -> StatusRead:
    LOG_APP.info(f"Attempting to update a status: {id}")
    db = request.state.db
    status = db.query(Status).filter(Status.id == id).first()

    raise_not_found_if_absent(status, f"Status with ID {id} not found")

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        LOG_APP.info(f"No update data provided for status: {id}")
        return StatusRead.model_validate(status)

    status.label = data.label
    db.commit()
    db.refresh(status)

    status_read = StatusRead.model_validate(status)
    LOG_APP.info(
        f"Status updated  successfully: {status_read.id} - {status_read.label}"
    )
    return status_read


@router.delete("/{id}")
async def delete_status(request: Request, id: int) -> None:
    LOG_APP.info(f"Attempting to delete a status: {id}")
    db = request.state.db
    status = db.query(Status).filter(Status.id == id).first()

    raise_not_found_if_absent(status, f"Status with ID {id} not found")

    db.delete(status)
    db.commit()
    LOG_APP.info(f"Status with ID {id} deleted successfully")
