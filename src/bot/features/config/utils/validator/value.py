"""Utility functions and classes for handling configuration values in Nightcore."""  # noqa

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from .transform import parse_csv_ints
from .transform import to_id as _to_id


class ValueKind(Enum):
    INT = auto()
    LIST_INT = auto()


@dataclass
class FieldSpec:
    field: str
    value: Any
    kind: ValueKind
    transform: Callable[[Any], Any] | None = None
    skip_if_none: bool = True


@dataclass
class Change:
    field: str
    old: Any
    new: Any
    changed: bool
    kind: ValueKind


def int_id_value(field: str, obj: Any | None) -> FieldSpec | None:
    """Creates a FieldSpec for an integer ID."""
    if obj is None:
        return None

    if isinstance(obj, int):
        return FieldSpec(field=field, value=obj, kind=ValueKind.INT)

    if hasattr(obj, "id"):
        return FieldSpec(
            field=field, value=obj, kind=ValueKind.INT, transform=_to_id
        )

    raise TypeError(
        f"int_id(): unsupported type for field {field}: {type(obj)!r}"
    )


def list_csv_value(
    field: str, csv: str | None, _len: int | None = None
) -> FieldSpec | None:
    """Creates a FieldSpec for a list of integers from a comma-separated string."""  # noqa: E501
    parsed = parse_csv_ints(csv)
    if _len is not None and parsed is not None and len(parsed) != _len:
        return None
    if parsed is None:
        return None

    return FieldSpec(field=field, value=parsed, kind=ValueKind.LIST_INT)
