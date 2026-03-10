"""Database models/other utilities."""

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .models import Karaoke


def cast_karaoke_model(value: object) -> "Karaoke":
    """Cast value to Karaoke model."""
    return cast("Karaoke", value)
