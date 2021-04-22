from copy import deepcopy
from typing import Dict

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.schema import Column

from app.infrastructure.db.entity import Base, _base_column


class Project(Base):
    __tablename__ = "project"

    id = Column("id", INTEGER(unsigned=True), primary_key=True, nullable=False)
    name = Column("name", VARCHAR(length=128), nullable=False)

    created_by = deepcopy(_base_column.created_by)
    updated_by = deepcopy(_base_column.updated_by)
    created_at = deepcopy(_base_column.created_at)
    updated_at = deepcopy(_base_column.updated_at)

    def to_dict(self) -> Dict:
        return {
            self.__class__.id.name: self.id,
            self.__class__.name.name: self.name,
        }
