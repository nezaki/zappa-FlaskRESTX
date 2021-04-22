from typing import Any, Dict, NoReturn

from sqlalchemy.orm import RelationshipProperty

# from app.infrastructure.db.entity._base_column import created_by


def payload_to_entity(table_class: Any, table_data: Any, payload: Dict) -> NoReturn:
    for v in vars(table_class):
        if not v.startswith("_") and hasattr(getattr(table_class, v), "key"):
            if v not in payload:
                continue

            if isinstance(getattr(table_class, v).property, RelationshipProperty):
                payload_to_entity(getattr(table_class, v).property.entity.class_, getattr(table_data, v), payload[v])
            else:
                setattr(table_data, v, payload[v])
    # if login_user:
    #     setattr(table_data, created_by.name, login_user.id)
