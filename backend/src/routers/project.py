from fastapi import APIRouter, Request, status
from sqlalchemy.orm import Session

from src.models import Project
from src.backend.config import LOG_APP
from src.routers.utils import raise_not_found_if_absent
from src.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create(request: Request, data: ProjectCreate) -> ProjectRead:
    LOG_APP.info("Attempting to create a project")
    db: Session = request.state.db

    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)

    project_read = ProjectRead.model_validate(project)
    LOG_APP.info(
        f"Project created successfully: {project_read.id} - {project_read.label}"
    )
    return project_read


@router.get("/{id}", response_model=ProjectRead)
async def get(request: Request, id: int) -> ProjectRead:
    LOG_APP.info(f"Attempting to get a project: {id}")
    db: Session = request.state.db
    project = db.query(Project).filter(Project.id == id).first()

    raise_not_found_if_absent(project, f"Project with ID {id} not found")

    project_read = ProjectRead.model_validate(project)
    LOG_APP.info(
        f"Project retrieved successfully: {project_read.id} - {project_read.label}"
    )
    return project_read


@router.get("/", response_model=list[ProjectRead])
async def get_all(request: Request) -> list[ProjectRead]:
    LOG_APP.info("Attempting to get all projects")
    db: Session = request.state.db
    projects = db.query(Project).all()

    raise_not_found_if_absent(projects, "No projects found")

    projects_read = [ProjectRead.model_validate(project) for project in projects]
    LOG_APP.info(f"Retrieved {len(projects_read)} projects from the database.")
    return projects_read


@router.put("/{id}", response_model=ProjectRead)
async def update(request: Request, id: int, data: ProjectUpdate) -> ProjectRead:
    LOG_APP.info(f"Attempting to update a project: {id}")
    db: Session = request.state.db
    project = db.query(Project).filter(Project.id == id).first()

    raise_not_found_if_absent(project, f"Project with ID {id} not found")

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        LOG_APP.info(f"No update data provided for project: {id}")
        return ProjectRead.model_validate(project)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    project_read = ProjectRead.model_validate(project)
    LOG_APP.info(
        f"Project updated successfully: {project_read.id} - {project_read.label}"
    )
    return project_read


@router.delete("/{id}")
async def delete(request: Request, id: int) -> None:
    LOG_APP.info(f"Attempting to delete a project: {id}")
    db: Session = request.state.db
    project = db.query(Project).filter(Project.id == id).first()

    raise_not_found_if_absent(project, f"Project with ID {id} not found")

    db.delete(project)
    db.commit()
    LOG_APP.info(f"Project with ID {id} deleted successfully")
