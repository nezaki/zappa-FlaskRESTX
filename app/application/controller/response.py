from http import HTTPStatus

from app.application.model.validation_error_model import ValidationErrors

OK = {
    "code": HTTPStatus.OK.value,
    "description": HTTPStatus.OK.description,
}

CREATED = {
    "code": HTTPStatus.CREATED.value,
    "description": HTTPStatus.CREATED.description,
}

NO_CONTENT = {
    "code": HTTPStatus.NO_CONTENT.value,
    "description": HTTPStatus.NO_CONTENT.description,
}

BAD_REQUEST = {
    "code": HTTPStatus.BAD_REQUEST.value,
    "model": ValidationErrors().model(),
    "description": HTTPStatus.BAD_REQUEST.description,
}

UNAUTHORIZED = {
    "code": HTTPStatus.UNAUTHORIZED.value,
    "description": HTTPStatus.UNAUTHORIZED.description,
}

FORBIDDEN = {
    "code": HTTPStatus.FORBIDDEN.value,
    "description": HTTPStatus.FORBIDDEN.description,
}

NOT_FOUND = {
    "code": HTTPStatus.NOT_FOUND.value,
    "description": HTTPStatus.NOT_FOUND.description,
}

CONFLICT = {
    "code": HTTPStatus.CONFLICT.value,
    "description": HTTPStatus.CONFLICT.description,
}
