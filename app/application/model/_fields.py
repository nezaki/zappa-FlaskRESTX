from datetime import datetime
from typing import Dict, Union

from flask_restx.fields import Boolean as OriginalBoolean
from flask_restx.fields import Date as OriginalDate
from flask_restx.fields import DateTime as OriginalDateTime
from flask_restx.fields import Float as OriginalFloat
from flask_restx.fields import Integer as OriginalInteger
from flask_restx.fields import List as OriginalList
from flask_restx.fields import Nested as OriginalNested
from flask_restx.fields import String as OriginalString

from app.application import pattern


class String(OriginalString):
    def __init__(self, *args, **kwargs):
        self.nullable = kwargs.pop("nullable", None)
        super(String, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]:
        schema = super(String, self).schema()
        schema.update(
            nullable=self._v("nullable"),
        )
        return schema


class Email(String):
    def __init__(self, *args, **kwargs):
        super(Email, self).__init__(*args, **kwargs)
        self.max_length = 255
        self.pattern = pattern.EMAIL
        self.example = "sample@examples.com"


class PictureType(String):
    def __init__(self, *args, **kwargs):
        super(PictureType, self).__init__(*args, **kwargs)
        self.max_length = 64
        self.enum = ["jpg", "png"]
        self.example = "jpg"


class Integer(OriginalInteger):
    def __init__(self, *args, **kwargs):
        self.nullable = kwargs.pop("nullable", None)
        super(Integer, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]:
        schema = super(Integer, self).schema()
        schema.update(
            nullable=self._v("nullable"),
        )
        return schema


class QueryInteger(OriginalInteger):
    def __init__(self, *args, **kwargs):
        super(QueryInteger, self).__init__(*args, **kwargs)


class Float(OriginalFloat):
    def __init__(self, *args, **kwargs):
        self.nullable = kwargs.pop("nullable", None)
        super(Float, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]:
        schema = super(Float, self).schema()
        schema.update(
            nullable=self._v("nullable"),
        )
        return schema


class Boolean(OriginalBoolean):
    def __init__(self, *args, **kwargs):
        self.nullable = kwargs.pop("nullable", None)
        super(Boolean, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]:
        schema = super(Boolean, self).schema()
        schema.update(
            nullable=self._v("nullable"),
        )
        return schema


class Date(OriginalDate):
    def __init__(self, *args, **kwargs):
        self.nullable = kwargs.pop("nullable", None)
        super(Date, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]:
        schema = super(Date, self).schema()
        schema.update(
            nullable=self._v("nullable"),
        )
        return schema


class DateTime(OriginalDateTime):
    def __init__(self, *args, **kwargs):
        self.nullable = kwargs.pop("nullable", None)
        super(DateTime, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]:
        schema = super(DateTime, self).schema()
        schema.update(
            nullable=self._v("nullable"),
        )
        return schema

    def format(self, value: datetime) -> str:
        return value.strftime(pattern.DATETIME)


class List(OriginalList):
    def __init__(self, *args, **kwargs):
        self.nullable = kwargs.pop("nullable", None)
        super(List, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]:
        schema = super(List, self).schema()
        schema.update(
            nullable=self._v("nullable"),
        )
        return schema


class Nested(OriginalNested):
    def __init__(self, *args, **kwargs):
        super(Nested, self).__init__(*args, **kwargs)

    def schema(self) -> Dict[str, Union[str, bool]]: # noqa
        schema = super(Nested, self).schema()
        return schema
