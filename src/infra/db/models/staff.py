"""Karaoke staff model."""

from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.enums import KaraokeRoleEnum
from src.infra.db.mixins import GuildIdMixin, UserIdMixin
from src.infra.db.models.base import BaseIdTimeStampModel


class Staff(BaseIdTimeStampModel, GuildIdMixin, UserIdMixin):
    """Karaoke staff role binding for a guild user."""

    __table_args__ = (
        UniqueConstraint(
            "guild_id",
            "user_id",
            "role",
            name="uq_karaoke_staff_guild_user_role",
        ),
    )

    role: Mapped[KaraokeRoleEnum] = mapped_column(
        Enum(
            KaraokeRoleEnum,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],  # type: ignore
            validate_strings=True,
        ),
        nullable=False,
    )
