from app.application import pattern
from app.application.model._enum_base import EnumBase
from app.application.model._fields import Boolean, DateTime, Integer, String
from app.application.model._model_base import ModelBase


class Status(EnumBase):
    TEMPORARILY_SAVED = "1", "一時保存"
    SAVED = "2", "保存"


class Example(ModelBase):
    __classname__ = "Example"

    example_string = String(
        title="example_string",
        description="文字列サンプル",
        required=True,
        nullable=False,
        example="サンプル",
        min_length=1,
        max_length=128,
        pattern=pattern.MATCH_ANYTHING,
        enum=None,
        readonly=False,
    )

    example_number = Integer(
        title="example_number",
        description="数値サンプル",
        required=False,
        nullable=False,
        example=1,
        min=1,
        max=4294967295,
        readonly=False,
    )

    example_datetime = DateTime(
        title="example_datetime",
        description="日時サンプル",
        required=False,
        nullable=False,
        example="2021-02-01T09:00:00+0000",
        readonly=False,
    )

    example_boolean = Boolean(
        title="example_boolean",
        description="真偽値サンプル",
        required=False,
        nullable=False,
        example=False,
        readonly=False,
    )

    example_enum = String(
        title="example_enum",
        description=f"状態<br>{Status.all_description()}",
        required=False,
        nullable=False,
        example="1",
        enum=Status.all(),
        readonly=False,
    )
