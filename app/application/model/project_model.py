from app.application import pattern
from app.application.model._fields import Integer, List, Nested, String
from app.application.model._model_base import ModelBase


class Project(ModelBase):
    __classname__ = "Project"

    id = Integer(
        title="id",
        description="ID",
        required=True,
        nullable=False,
        example=1,
        min=1,
        max=4294967295,
        readonly=True,
    )

    name = String(
        title="name",
        description="名前",
        required=True,
        nullable=False,
        example="テストプロジェクト",
        min_length=1,
        max_length=128,
        pattern=pattern.MATCH_ANYTHING,
        enum=None,
        readonly=False,
    )


class Projects(ModelBase):
    __classname__ = "Projects"

    organizations = List(
        title="projects",
        cls_or_instance=Nested(
            model=Project().model(),
            required=True,
            allow_null=False,
            skip_none=False,
            readonly=True,
            as_list=False,
        ),
        min_items=0,
        max_items=1000,
        unique=True,
        required=True
    )
