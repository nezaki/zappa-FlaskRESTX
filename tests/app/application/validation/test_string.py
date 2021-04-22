import random
import string

from app.application.model._fields import String
from app.application.validation import Validator


def get_random_str(num: int) -> str:
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return "".join([random.choice(dat) for i in range(num)])


class TestString(object):
    @staticmethod
    def _is_error(value, field):  # noqa: ANN001, ANN205
        validator = Validator()
        validator.string(value, field)
        return validator.has_errors()

    def test(self):  # noqa: ANN201
        not_nullable_field = String(nullable=False)
        assert not TestString._is_error("テスト", not_nullable_field)
        assert not TestString._is_error("", not_nullable_field)
        assert TestString._is_error(None, not_nullable_field)

        min_length_field = String(min_length=1)
        assert not TestString._is_error("テスト", min_length_field)
        assert TestString._is_error("", min_length_field)
        assert TestString._is_error(None, min_length_field)

        max_length_field = String(max_length=1)
        assert TestString._is_error("テスト", max_length_field)
        assert not TestString._is_error("", max_length_field)

        min_max_length_field = String(min_length=8, max_length=32)
        assert TestString._is_error(get_random_str(7), min_max_length_field)
        assert not TestString._is_error(get_random_str(8), min_max_length_field)
        assert not TestString._is_error(get_random_str(9), min_max_length_field)
        assert not TestString._is_error(get_random_str(31), min_max_length_field)
        assert not TestString._is_error(get_random_str(32), min_max_length_field)
        assert TestString._is_error(get_random_str(33), min_max_length_field)

        pattern_field = String(pattern=r"^[a-zA-Z0-9]+$")
        assert TestString._is_error("テスト", pattern_field)
        assert not TestString._is_error("Test1234", pattern_field)
        assert TestString._is_error("Test_1234", pattern_field)

        enum_field = String(enum=["1", "2", "3"])
        assert TestString._is_error("0", enum_field)
        assert not TestString._is_error("1", enum_field)
        assert not TestString._is_error("2", enum_field)
        assert not TestString._is_error("3", enum_field)
        assert TestString._is_error("4", enum_field)
