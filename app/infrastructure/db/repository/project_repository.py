from typing import List, NoReturn, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.infrastructure.db.entity.project import Project


def find_by_id(db_session: Session, id_: int) -> Optional[Project]:
    try:
        return db_session.query(Project).filter(Project.id == id_).one()
    except NoResultFound:
        return None


def find_all(db_session: Session) -> Optional[List[Project]]:
    return db_session.query(Project).all()


def create(db_session: Session, project: Project) -> NoReturn:
    db_session.add(project)


def delete(db_session: Session, deleting_id: int) -> NoReturn:
    db_session.query(Project).filter(Project.id == deleting_id).delete()
