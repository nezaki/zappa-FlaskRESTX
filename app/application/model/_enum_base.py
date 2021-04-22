from enum import Enum
from typing import List


class EnumBase(Enum):
    def __new__(cls, value: str, description: str = ""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def all(cls) -> List[str]:  # noqa: ANN102
        return [c.value for c in list(cls.__members__.values())]

    @classmethod
    def all_description(cls) -> str:  # noqa: ANN102
        list_ = [f"{c.value}: {c.description}" for c in list(cls.__members__.values())]
        return "<br>".join(list_)
