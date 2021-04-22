from sqlalchemy import text
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import current_timestamp

created_by = Column("created_by", INTEGER(unsigned=True), nullable=False)
updated_by = Column("updated_by", INTEGER(unsigned=True), nullable=True)
created_at = Column("created_at", TIMESTAMP(), nullable=False, server_default=current_timestamp())
updated_at = Column("updated_at", TIMESTAMP(), nullable=True, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))
