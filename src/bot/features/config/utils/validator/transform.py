"""Utility functions for transforming and validating configuration values."""

from typing import Any


def to_id(obj: Any) -> int:
    """Extracts an integer ID from an object."""
    return obj.id


def parse_csv_ints(s: str | None, sep: str = ",") -> list[int] | None:
    """Parses a comma-separated string of integers into a list of integers."""
    if not s:
        return None
    out: set[int] = set()
    for part in s.split(sep):
        part = part.strip()
        if not part:
            continue
        try:
            out.add(int(part))
        except ValueError:
            continue
    return list(out) or None
