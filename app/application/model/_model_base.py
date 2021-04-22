import typing
from copy import deepcopy

from flask_restx import Model


class ModelBase(object):

    def model(self, name: typing.Optional[str] = None, excludes: typing.Optional[typing.List[str]] = None) -> Model:
        d = {}
        for attr_name in dir(self.__class__):
            if attr_name.startswith("__"):
                continue
            attr = getattr(self.__class__, attr_name)
            if not hasattr(attr, "title"):
                continue
            if excludes is not None and attr.title in excludes:
                continue
            d[attr.title] = deepcopy(attr)
        return Model(self.__classname__ if not name else name, d)  # noqa: T484
