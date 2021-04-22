from copy import deepcopy

from sqlalchemy import text
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.schema import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.functions import current_timestamp

created_by = Column("created_by", INTEGER(unsigned=True), nullable=False)
updated_by = Column("updated_by", INTEGER(unsigned=True), nullable=True)
created_at = Column("created_at", TIMESTAMP(), nullable=False, server_default=current_timestamp())
updated_at = Column("updated_at", TIMESTAMP(), nullable=True, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))


meta = MetaData()

project = Table(
    "project", meta,
    Column("id", INTEGER(unsigned=True), nullable=False, autoincrement=True, primary_key=True),
    Column("name", VARCHAR(128), nullable=False),
    deepcopy(created_by), deepcopy(updated_by), deepcopy(created_at), deepcopy(updated_at)
)

user = Table(
    "user", meta,
    Column("id", INTEGER(unsigned=True), nullable=False, autoincrement=True, primary_key=True),
    Column("name", VARCHAR(128), nullable=False),
    deepcopy(created_by), deepcopy(updated_by), deepcopy(created_at), deepcopy(updated_at)
)

project_user = Table(
    "project_user", meta,
    Column("project_id", INTEGER(unsigned=True), ForeignKey("project.id", onupdate="CASCADE", ondelete="CASCADE"),
           primary_key=True, nullable=False),
    Column("user_id", INTEGER(unsigned=True), ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
           primary_key=True, nullable=False),
    deepcopy(created_by), deepcopy(updated_by), deepcopy(created_at), deepcopy(updated_at)
)

issue_category = Table(
    "issue_category", meta,
    Column("id", INTEGER(unsigned=True), nullable=False, autoincrement=True, primary_key=True),
    Column("name", VARCHAR(128), nullable=False),
    deepcopy(created_by), deepcopy(updated_by), deepcopy(created_at), deepcopy(updated_at)
)

issue = Table(
    "issue", meta,
    Column("id", INTEGER(unsigned=True), nullable=False, autoincrement=True, primary_key=True),
    Column("project_id", INTEGER(unsigned=True), ForeignKey("project.id", onupdate="CASCADE", ondelete="CASCADE"),
           primary_key=True, nullable=False),
    Column("user_id", INTEGER(unsigned=True), ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
           primary_key=True, nullable=False),
    Column("issue_category_id", INTEGER(unsigned=True),
           ForeignKey("issue_category.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False),
    Column("title", VARCHAR(64), nullable=False),
    Column("description", VARCHAR(128), nullable=True),
    Column("status", VARCHAR(2), nullable=False),
    deepcopy(created_by), deepcopy(updated_by), deepcopy(created_at), deepcopy(updated_at)
)


def upgrade(migrate_engine):  # noqa
    meta.bind = migrate_engine

    migrate_engine.execute(text("SET SESSION sql_mode = '';"))

    project.create()
    user.create()
    project_user.create()
    issue_category.create()
    issue.create()


def downgrade(migrate_engine):  # noqa
    meta.bind = migrate_engine

    issue.drop()
    issue_category.drop()
    project_user.drop()
    user.drop()
    project.drop()
