from fastapi import APIRouter, Depends, Request, status, Body, Path
from sqlalchemy.orm import Session
from src.models import Ticket
from src.backend.config import LOG_APP
from src.routers.utils import get_db, raise_not_found_if_absent
from src.schemas._ticket import TicketCreate, TicketRead, TicketUpdate


router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create(data: TicketCreate, db: Session = Depends(get_db)) -> TicketRead:
    LOG_APP.info(f"Attempting to create a ticket {data.title}")

    ticket = Ticket(
        title=data.title,
        description=data.description,
        creator_id=data.creator_id,
        project_id=data.project_id,
        status_id=data.status_id,
        category_id=data.category_id,
        level_id=data.level_id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    ticket_read = TicketRead.model_validate(ticket)
    LOG_APP.info(f"Ticket created successfully: {ticket_read.id} - {ticket_read.title}")
    return ticket_read


@router.get("/{id}", response_model=TicketRead)
async def get(id: int = Path(...), db: Session = Depends(get_db)) -> TicketRead:
    LOG_APP.info(f"Attempting to get a ticket: {id}")
    ticket = db.query(Ticket).filter(Ticket.id == id).first()

    raise_not_found_if_absent(ticket, f"Ticket with ID {id} not found")

    ticket_read = TicketRead.model_validate(ticket)
    LOG_APP.info(
        f"Ticket retrieved successfully: {ticket_read.id} - {ticket_read.title}"
    )
    return ticket_read


@router.get("/", response_model=list[TicketRead])
async def get_all(db: Session = Depends(get_db)) -> list[TicketRead]:
    LOG_APP.info("Attempting to get all tickets")

    tickets = db.query(Ticket).all()

    raise_not_found_if_absent(tickets, "No tickets found")

    tickets_read = [TicketRead.model_validate(ticket) for ticket in tickets]
    LOG_APP.info(f"Retrieved {len(tickets_read)} tickets from the database.")
    return tickets_read


@router.put("/{id}", response_model=TicketRead)
async def update(
    id: int = Path(...), data: TicketUpdate = Body(...), db: Session = Depends(get_db)
) -> TicketRead:
    LOG_APP.info(f"Attempting to update a ticket: {id}")
    ticket = db.query(Ticket).filter(Ticket.id == id).first()

    raise_not_found_if_absent(ticket, f"Ticket with ID {id} not found")

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        LOG_APP.info(f"No update data provided for ticket: {id}")
        return TicketRead.model_validate(ticket)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    ticket_read = TicketRead.model_validate(ticket)
    LOG_APP.info(f"Ticket updated successfully: {ticket_read.id} - {ticket_read.title}")
    return ticket_read


@router.delete("/{id}")
async def delete(id: int = Path(...), db: Session = Depends(get_db)) -> None:
    LOG_APP.info(f"Attempting to delete a ticket: {id}")
    ticket = db.query(Ticket).filter(Ticket.id == id).first()

    raise_not_found_if_absent(ticket, f"Ticket with ID {id} not found")

    db.delete(ticket)
    db.commit()
    LOG_APP.info(f"Ticket with ID {id} deleted successfully")
