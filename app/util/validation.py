import re
from datetime import datetime
from typing import Any, List


def is_string_type(value: Any) -> bool:
    return isinstance(value, str)


def is_integer_type(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_float_type(value: Any) -> bool:
    return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)


def is_boolean_type(value: Any) -> bool:
    return isinstance(value, bool)


def is_date_type(value: Any, pattern_str: str) -> bool:
    return is_datetime_type(value, pattern_str)


def is_datetime_type(value: Any, pattern_str: str) -> bool:
    try:
        datetime.strptime(value, pattern_str)
    except Exception:
        return False
    return True


def min_length(value: str, length: int) -> bool:
    if length <= len(value):
        return True
    return False


def max_length(value: str, length: int) -> bool:
    if len(value) <= length:
        return True
    return False


def minimum(value: int, minimum_value: int) -> bool:
    if minimum_value <= value:
        return True
    return False


def exclusive_minimum(value: int, minimum_value: int) -> bool:
    if minimum_value < value:
        return True
    return False


def maximum(value: int, maximum_value: int) -> bool:
    if value <= maximum_value:
        return True
    return False


def exclusive_maximum(value: int, maximum_value: int) -> bool:
    if value < maximum_value:
        return True
    return False


def pattern(value: str, pattern_str: str) -> bool:
    return bool(re.fullmatch(pattern_str, value))


def is_contained(value: str, enum_values: List[str]) -> bool:
    return value in enum_values


def full_match(value: str, pattern_str: str) -> bool:
    pattern_ = re.compile(pattern_str)
    return pattern_.fullmatch(value) is not None
