from typing import NoReturn, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.infrastructure.db.entity.project import Project


def find_by_id(db_session: Session, id_: int) -> Optional[Project]:
    try:
        return db_session.query(Project).filter(Project.id == id_).one()
    except NoResultFound:
        return None


def create(db_session: Session, project: Project) -> NoReturn:
    db_session.add(project)
