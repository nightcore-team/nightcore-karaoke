"""Database enums."""

from enum import Enum


class StrEnum(str, Enum):
    """String enum."""

    def __str__(self) -> str:
        """Return the string representation of the enum."""
        return self.value


class KaraokeStateEnum(StrEnum):
    """Karaoke status enum."""

    ANNOUNCED = "announced"
    GOING = "going"
    FINISHED = "finished"


class KaraokeRegistrationStateEnum(StrEnum):
    """Karaoke registration status enum."""

    OPEN = "open"
    CLOSED = "closed"


class KaraokeRoleEnum(StrEnum):
    """Karaoke role enum."""

    HOST = "host"
    JUDGE = "judge"
