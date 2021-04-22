from app.application.model._fields import Integer
from app.application.validation import Validator


class TestInteger(object):

    @staticmethod
    def _is_error(value, field):  # noqa: ANN001, ANN205
        validator = Validator()
        validator.integer(value, field)
        return validator.has_errors()

    def test(self):  # noqa: ANN201
        not_nullable_field = Integer(nullable=False)
        assert not TestInteger._is_error(1, not_nullable_field)
        assert not TestInteger._is_error(0, not_nullable_field)
        assert not TestInteger._is_error(-1, not_nullable_field)
        assert TestInteger._is_error(None, not_nullable_field)

        assert TestInteger._is_error("test", not_nullable_field)

        min_field = Integer(min=1)
        assert TestInteger._is_error(0, min_field)
        assert not TestInteger._is_error(1, min_field)
        assert not TestInteger._is_error(2, min_field)

        max_field = Integer(max=1)
        assert not TestInteger._is_error(0, max_field)
        assert not TestInteger._is_error(1, max_field)
        assert TestInteger._is_error(2, max_field)

        min_max_field = Integer(min=10, max=11)
        assert TestInteger._is_error(9, min_max_field)
        assert not TestInteger._is_error(10, min_max_field)
        assert not TestInteger._is_error(11, min_max_field)
        assert TestInteger._is_error(12, min_max_field)

        exclusive_min_field = Integer(exclusiveMin=100)
        assert TestInteger._is_error(99, exclusive_min_field)
        assert TestInteger._is_error(100, exclusive_min_field)
        assert not TestInteger._is_error(101, exclusive_min_field)

        exclusive_max_field = Integer(exclusiveMax=200)
        assert not TestInteger._is_error(199, exclusive_max_field)
        assert TestInteger._is_error(200, exclusive_max_field)
        assert TestInteger._is_error(201, exclusive_max_field)

        exclusive_min_max_field = Integer(exclusiveMin=300, exclusiveMax=302)
        assert TestInteger._is_error(299, exclusive_min_max_field)
        assert TestInteger._is_error(300, exclusive_min_max_field)
        assert not TestInteger._is_error(301, exclusive_min_max_field)
        assert TestInteger._is_error(302, exclusive_min_max_field)
        assert TestInteger._is_error(303, exclusive_min_max_field)
