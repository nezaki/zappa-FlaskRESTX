from flask_restx import Model

from app.application.model._fields import String
from app.application.validation import validate


class TestValidate(object):
    @staticmethod
    def _is_error(model, payload):  # noqa: ANN001, ANN205
        try:
            validate(model, payload)
        except:  # noqa: E722
            return True
        return False

    def test(self):  # noqa: ANN201
        model = None
        payload = None
        assert TestValidate._is_error(model, payload)

        model = None
        payload = "test"
        assert TestValidate._is_error(model, payload)

        # readonly=True
        field = String(title="field", nullable=False, readonly=True)
        model = Model("TestModel", {"field": field})
        payload = {"field": None}
        assert not TestValidate._is_error(model, payload)

        # not exists field
        field = String(title="field", nullable=False, readonly=False)
        model = Model("TestModel", {"field": field})
        payload = {"field_dummy": None}
        assert not TestValidate._is_error(model, payload)

        # nullable
        field = String(title="field", nullable=True, readonly=False)
        model = Model("TestModel", {"field": field})
        payload = {"field": None}
        assert not TestValidate._is_error(model, payload)
