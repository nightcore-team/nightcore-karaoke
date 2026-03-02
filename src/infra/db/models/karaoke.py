"""Karaoke model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.enums import KaraokeRegistrationStateEnum, KaraokeStateEnum
from src.infra.db.mixins import GuildIdMixin
from src.infra.db.models.base import BaseIdTimeStampModel

if TYPE_CHECKING:
    from src.infra.db.models.rating import Rating
    from src.infra.db.models.registration import Registration


class Karaoke(BaseIdTimeStampModel, GuildIdMixin):
    """Karaoke model."""

    __table_args__ = (
        Index(
            "uq_karaoke_guild_active",
            "guild_id",
            unique=True,
            postgresql_where=text("state <> 'finished'"),
        ),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[KaraokeStateEnum] = mapped_column(
        Enum(
            KaraokeStateEnum,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],  # type: ignore
            validate_strings=True,
        ),
        nullable=False,
    )
    registration_state: Mapped[KaraokeRegistrationStateEnum] = mapped_column(
        Enum(
            KaraokeRegistrationStateEnum,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],  # type: ignore
            validate_strings=True,
        ),
        nullable=False,
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="karaoke",
        cascade="all, delete-orphan",
    )
    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="karaoke",
        cascade="all, delete-orphan",
    )
