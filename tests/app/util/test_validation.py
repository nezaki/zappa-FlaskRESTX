from datetime import datetime
from typing import Callable, List, NoReturn

from app.application import pattern
from app.util import validation

_test_values = [
    "",
    "a",
    b"a",
    -1,
    0,
    1,
    1.0,
    True,
    False,
    "2021-04-21",
    datetime(year=2021, month=4, day=21),
    "2021-05-22T09:24:46+0900",
    datetime(year=2022, month=5, day=22, hour=9, minute=24, second=46),
    [],
    {},
    (),
    None,
]


def _test(func: Callable, returns: List[bool]) -> NoReturn:
    for index, value in enumerate(_test_values):
        assert func(value) == returns[index]


def test_is_string_type() -> NoReturn:
    _test(
        func=validation.is_string_type,
        returns=[True, True, False, False, False, False, False, False, False, True, False, True, False, False,
                 False, False, False]
    )


def test_is_integer_type() -> NoReturn:
    _test(
        func=validation.is_integer_type,
        returns=[False, False, False, True, True, True, False, False, False, False, False, False, False, False,
                 False, False, False]
    )


def test_is_float_type() -> NoReturn:
    _test(
        func=validation.is_float_type,
        returns=[False, False, False, True, True, True, True, False, False, False, False, False, False, False,
                 False, False, False]
    )


def test_is_boolean_type() -> NoReturn:
    _test(
        func=validation.is_boolean_type,
        returns=[False, False, False, False, False, False, False, True, True, False, False, False, False, False,
                 False, False, False]
    )


def test_is_date_type() -> NoReturn:
    returns = [False, False, False, False, False, False, False, False, False, True, False, False, False, False,
               False, False, False]
    for index, value in enumerate(_test_values):
        assert validation.is_date_type(value, pattern.DATE) == returns[index]


def test_is_datetime_type() -> NoReturn:
    returns = [False, False, False, False, False, False, False, False, False, False, False, True, False, False,
               False, False, False]
    for index, value in enumerate(_test_values):
        assert validation.is_datetime_type(value, pattern.DATETIME) == returns[index]


def test_min_length() -> NoReturn:
    value = "min-test"
    assert validation.min_length(value, 7)
    assert validation.min_length(value, 8)
    assert not validation.min_length(value, 9)


def test_max_length() -> NoReturn:
    value = "test"
    assert not validation.max_length(value, 3)
    assert validation.max_length(value, 4)
    assert validation.max_length(value, 5)


def test_minimum() -> NoReturn:
    value = 128
    assert validation.minimum(value, 127)
    assert validation.minimum(value, 128)
    assert not validation.minimum(value, 129)


def test_exclusive_minimum() -> NoReturn:
    value = 256
    assert validation.exclusive_minimum(value, 255)
    assert not validation.exclusive_minimum(value, 256)
    assert not validation.exclusive_minimum(value, 257)


def test_maximum() -> NoReturn:
    value = 128
    assert not validation.maximum(value, 127)
    assert validation.maximum(value, 128)
    assert validation.maximum(value, 129)


def test_exclusive_maximum() -> NoReturn:
    value = 256
    assert not validation.exclusive_maximum(value, 255)
    assert not validation.exclusive_maximum(value, 256)
    assert validation.exclusive_maximum(value, 257)


def test_pattern() -> NoReturn:
    assert validation.pattern("test@example.com", pattern.EMAIL)
    assert not validation.pattern("pattern_test", pattern.EMAIL)


def test_is_contained() -> NoReturn:
    enum_values = ["1", "2", "3"]
    assert not validation.is_contained("0", enum_values)
    assert validation.is_contained("1", enum_values)
    assert validation.is_contained("2", enum_values)
    assert validation.is_contained("3", enum_values)
    assert not validation.is_contained("4", enum_values)


def test_full_match() -> NoReturn:
    assert validation.full_match("test@example.com", pattern.EMAIL)
    assert not validation.full_match("pattern_test", pattern.EMAIL)
