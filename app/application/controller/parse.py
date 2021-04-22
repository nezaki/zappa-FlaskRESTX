from datetime import datetime
from functools import wraps
from typing import Dict, Optional

from flask import request
from flask_restx import Model

from app.application import pattern
from app.application.model._fields import DateTime, List, Nested
from app.application.validation import validate


def _parse_payload(model: Dict, payload: Dict, http_method: str) -> Dict:
    parsed_payload = {}
    for title, field in model.items():
        if field.readonly or title not in payload:
            continue
        if isinstance(field, DateTime):
            if payload[title]:
                parsed_payload[title] = datetime.strptime(payload[title], pattern.DATETIME)
        elif isinstance(field, Nested):
            if payload[title]:
                parsed_payload[title] = _parse_payload(field.model, payload[title], http_method)
        elif isinstance(field, List):
            # TODO
            pass
        else:
            if title in payload:
                parsed_payload[title] = payload[title]
    return parsed_payload


def parse_payload(model: Optional[Model]):  # noqa: ANN201
    def decorator(func):  # noqa: ANN001, ANN201
        @wraps(func)  # noqa: ANN001, ANN201
        def wrapper(*args, **kwargs):  # noqa: ANN201
            payload = request.get_json()
            validate(model, payload)
            response = func(*args, **kwargs, payload=_parse_payload(model, payload, func.__name__))
            return response
        return wrapper
    return decorator
