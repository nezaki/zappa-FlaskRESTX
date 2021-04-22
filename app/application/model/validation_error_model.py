import typing

from app.application.error_code import ErrorCode
from app.application.model._fields import List, Nested, String
from app.application.model._model_base import ModelBase


class ValidationError(ModelBase):

    __classname__ = "ValidationError"

    field = String(
        title="field",
        description="フィールド名",
        required=True,
        nullable=False,
        example="name",
    )
    code = List(
        title="code",
        cls_or_instance=String(
            description="エラーコード",
            required=True,
            enum=[e.value for e in ErrorCode],
        ),
        required=True,
        nullable=False,
        example=[ErrorCode.REQUIRED.value],
    )

    @staticmethod
    def format(field: str, code: typing.List[ErrorCode]) -> typing.Dict:
        return {
            ValidationError.field.title: field,
            ValidationError.code.title: [e.value for e in code],
        }


class ValidationErrors(ModelBase):
    __classname__ = "ValidationErrors"

    errors = List(
        title="errors",
        cls_or_instance=Nested(
            model=ValidationError().model(),
            required=True,
            allow_null=False,
            skip_none=False,
            readonly=True,
            as_list=False,
        ),
        required=True,
        nullable=False,
    )
