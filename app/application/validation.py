import typing
from http import HTTPStatus

import flask_restx
from flask_restx import Model

from app.application import pattern
from app.application.error_code import ErrorCode
from app.application.model._fields import Boolean, Date, DateTime, Float, Integer, String
from app.application.model.validation_error_model import ValidationError
from app.util.validation import (
    full_match,
    is_boolean_type,
    is_contained,
    is_date_type,
    is_datetime_type,
    is_float_type,
    is_integer_type,
    is_string_type,
    max_length,
    maximum,
    min_length,
    minimum,
)


class Validator:
    def __init__(self): # noqa
        self.errors: typing.List = []

    def has_errors(self) -> bool:
        return bool(self.errors)

    def abort(self, code: int = HTTPStatus.BAD_REQUEST.value) -> typing.NoReturn:
        flask_restx.abort(
            code=code,
            errors=self.errors,
        )

    def add_errors(self, field: str, code: typing.List[ErrorCode]) -> typing.NoReturn:
        self.errors.append(ValidationError.format(field, code))

    def get_errors(self) -> typing.List:
        return self.errors

    def string(self, value: typing.Optional[typing.Any], field: String) -> typing.NoReturn:
        error_codes: typing.List[ErrorCode] = []

        if field.nullable is not None and not field.nullable:
            if value is None:
                self.add_errors(field=field.title, code=[ErrorCode.NOT_NULL])
                return

        if not is_string_type(value):
            self.add_errors(field=field.title, code=[ErrorCode.NOT_STRING])
            return

        if field.min_length and field.max_length:
            if not min_length(value, field.min_length) or not max_length(value, field.max_length):
                error_codes.append(ErrorCode.MIN_MAX_LENGTH)
        elif field.min_length:
            if not min_length(value, field.min_length):
                error_codes.append(ErrorCode.MIN_LENGTH)
        elif field.max_length:
            if not max_length(value, field.max_length):
                error_codes.append(ErrorCode.MAX_LENGTH)

        if field.enum:
            if not is_contained(value, field.enum):
                error_codes.append(ErrorCode.ENUM)

        if field.pattern and field.pattern != pattern.MATCH_ANYTHING:
            if not full_match(value, field.pattern):
                error_codes.append(ErrorCode.PATTERN)

        if error_codes:
            self.add_errors(field=field.title, code=error_codes)

    def integer(self, value: typing.Optional[typing.Any], field: Integer) -> None:
        error_codes: typing.List[ErrorCode] = []

        if field.nullable is not None and field.nullable:
            if value is None:
                return

        if field.nullable is not None and not field.nullable:
            if value is None:
                self.add_errors(field=field.title, code=[ErrorCode.NOT_NULL])
                return

        if not is_integer_type(value):
            self.add_errors(field=field.title, code=[ErrorCode.NOT_INTEGER])
            return

        if field.minimum and field.maximum:
            if not minimum(value, field.minimum) or not maximum(value, field.maximum):
                error_codes.append(ErrorCode.MIN_MAX)
        elif field.minimum:
            if not minimum(value, field.minimum):
                error_codes.append(ErrorCode.MIN)
        elif field.maximum:
            if not maximum(value, field.maximum):
                error_codes.append(ErrorCode.MAX)

        if error_codes:
            self.add_errors(field=field.title, code=error_codes)

    def float(self, value: typing.Optional[typing.Any], field: Float) -> None:
        error_codes: typing.List[ErrorCode] = []

        if field.nullable is not None and field.nullable:
            if value is None:
                return

        if field.nullable is not None and not field.nullable:
            if value is None:
                self.add_errors(field=field.title, code=[ErrorCode.NOT_NULL])
                return

        if not is_float_type(value):
            self.add_errors(field=field.title, code=[ErrorCode.NOT_FLOAT])
            return

        if field.minimum and field.maximum:
            if not minimum(value, field.minimum) or not maximum(value, field.maximum):
                error_codes.append(ErrorCode.MIN_MAX)
        elif field.minimum:
            if not minimum(value, field.minimum):
                error_codes.append(ErrorCode.MIN)
        elif field.maximum:
            if not maximum(value, field.maximum):
                error_codes.append(ErrorCode.MAX)

        if error_codes:
            self.add_errors(field=field.title, code=error_codes)

    def boolean(self, value: typing.Optional[typing.Any], field: Boolean) -> None:
        error_codes: typing.List[ErrorCode] = []

        if not is_boolean_type(value):
            error_codes.append(ErrorCode.NOT_BOOLEAN)

        if error_codes:
            self.add_errors(field=field.title, code=error_codes)

    def date(self, value: typing.Optional[typing.Any], field: Date) -> None:
        error_codes: typing.List[ErrorCode] = []

        if not is_date_type(value, pattern.DATE):
            error_codes.append(ErrorCode.NOT_DATE)

        if error_codes:
            self.add_errors(field=field.title, code=error_codes)

    def datetime(self, value: typing.Optional[typing.Any], field: DateTime) -> None:
        error_codes: typing.List[ErrorCode] = []

        if not is_datetime_type(value, pattern.DATETIME):
            error_codes.append(ErrorCode.NOT_DATETIME)

        if error_codes:
            self.add_errors(field=field.title, code=error_codes)


def validate(model: Model, payload: typing.Optional[typing.Any]) -> None:
    validator = Validator()

    if payload is None or not isinstance(payload, typing.Dict):
        validator.add_errors(field="payload", code=[ErrorCode.REQUIRED])  # TODO 内容の精査
        validator.abort()
        return

    for title, field in model.items():
        # TODO Listで受け付ける場合の対応

        if field.readonly:
            continue

        if field.title not in payload:
            if field.required:
                validator.add_errors(field=field.title, code=[ErrorCode.REQUIRED])
            continue

        if field.nullable and payload.get(title) is None:
            continue

        if isinstance(field, String):
            validator.string(payload.get(title), field)
        elif isinstance(field, Integer):
            validator.integer(payload.get(title), field)
        elif isinstance(field, Float):
            validator.float(payload.get(title), field)
        elif isinstance(field, Boolean):
            validator.boolean(payload.get(title), field)
        elif isinstance(field, Date):
            validator.date(payload.get(title), field)
        elif isinstance(field, DateTime):
            validator.datetime(payload.get(title), field)

    if validator.has_errors():
        validator.abort()
