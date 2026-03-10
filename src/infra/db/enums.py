"""Database enums."""

from enum import Enum


class StrEnum(str, Enum):
    """String enum."""

    def __str__(self) -> str:
        """Return the string representation of the enum."""
        return self.value


class KaraokeStateEnum(StrEnum):
    """Karaoke status enum."""

    ANNOUNCED = "Анонсировано"
    GOING = "Идет"
    FINISHED = "Завершено"


class KaraokeRegistrationStateEnum(StrEnum):
    """Karaoke registration status enum."""

    OPEN = "Открыта"
    CLOSED = "Закрыта"


class KaraokeRoleEnum(StrEnum):
    """Karaoke role enum."""

    HOST = "host"
    JUDGE = "judge"
