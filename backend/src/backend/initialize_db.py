import random
from faker import Faker
from sqlalchemy.orm import Session

from src.backend.config import ENGINE, LOG_APP
from src.models import Base, Category, Level, Status, User, Project, Ticket, Comment


fake = Faker()

CATEGORY_COUNT = 10
LEVEL_COUNT = 3
STATUS_COUNT = 3
TICKET_COUNT = 500
USER_COUNT = 100
PROJECT_COUNT = 10
COMMENT_COUNT = 1000


def insert_default_categories(db: Session):
    LOG_APP.info("Inserting default categories")

    categories = [
        "Bogue",
        "Ajout fonction",
        "Amélioration",
        "Tâche",
        "Documentation",
        "Performance",
        "Sécurité",
        "Interface UI",
        "Test",
        "Configuration",
    ]
    db.query(Category).delete()
    db.bulk_save_objects([Category(label=label) for label in categories])
    LOG_APP.info("Default categories inserted successfully")


def insert_default_levels(db: Session):
    LOG_APP.info("Inserting default levels")
    levels = [
        "Faible",
        "Moyen",
        "Élevé",
    ]
    db.query(Level).delete()
    db.bulk_save_objects([Level(label=label) for label in levels])
    LOG_APP.info("Default levels inserted successfully")


def insert_default_statuses(db: Session):
    LOG_APP.info("Inserting default statuses")
    statuses = [
        "Ouvert",
        "En cours",
        "Terminé",
    ]
    db.query(Status).delete()
    db.bulk_save_objects([Status(label=label) for label in statuses])
    LOG_APP.info("Default statuses inserted successfully")


def insert_users(db: Session):
    LOG_APP.info("Generating users")
    users = [
        User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.user_name(),
            email=fake.email(),
            role=random.choice(
                ["user", "admin", "manager", "developer", "designer", "tester"]
            ),
            password=fake.password(
                length=12,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        )
        for _ in range(USER_COUNT)
    ]
    db.query(User).delete()
    db.bulk_save_objects(users)
    LOG_APP.info(f"{len(users)} users inserted successfully.")


def insert_projects(db: Session):
    LOG_APP.info("Generating projects")
    projects = [
        Project(
            label=fake.word(),
            description=fake.sentence(),
            creator_id=random.randint(1, USER_COUNT),
        )
        for _ in range(PROJECT_COUNT)
    ]
    db.query(Project).delete()
    db.bulk_save_objects(projects)
    LOG_APP.info(f"{len(projects)} projects inserted successfully.")


def insert_tickets(db: Session):
    LOG_APP.info("Generating tickets")
    tickets = [
        Ticket(
            title=fake.sentence(),
            description=fake.sentence(),
            creator_id=random.randint(1, USER_COUNT),
            project_id=random.randint(1, PROJECT_COUNT),
            status_id=random.randint(1, STATUS_COUNT),
            category_id=random.randint(1, CATEGORY_COUNT),
            level_id=random.randint(1, LEVEL_COUNT),
        )
        for _ in range(TICKET_COUNT)
    ]
    db.query(Ticket).delete()
    db.bulk_save_objects(tickets)
    LOG_APP.info(f"{len(tickets)} tickets inserted successfully.")


def insert_comments(db: Session):
    LOG_APP.info("Generating comments")
    comments = [
        Comment(
            content=fake.sentence(),
            creator_id=random.randint(1, USER_COUNT),
            ticket_id=random.randint(1, TICKET_COUNT),
        )
        for _ in range(COMMENT_COUNT)
    ]
    db.query(Comment).delete()
    db.bulk_save_objects(comments)
    LOG_APP.info(f"{len(comments)} comments inserted successfully.")


def initialize_db():
    Base.metadata.create_all(bind=ENGINE)
    with Session(ENGINE) as session:
        session.begin()
        try:
            insert_default_categories(session)
            insert_default_levels(session)
            insert_default_statuses(session)
            insert_users(session)
            insert_projects(session)
            insert_tickets(session)
            insert_comments(session)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error during initialization: {e}")
        finally:
            session.close()


if __name__ == "__main__":
    initialize_db()
