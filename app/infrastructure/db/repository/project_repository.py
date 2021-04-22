from typing import NoReturn

from sqlalchemy.orm.session import Session

from app.infrastructure.db.entity.project import Project


def create(db_session: Session, project: Project) -> NoReturn:
    db_session.add(project)
