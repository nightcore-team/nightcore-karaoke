"""Registration model."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.mixins import GuildIdMixin, UserIdMixin
from src.infra.db.models.base import BaseIdTimeStampModel

if TYPE_CHECKING:
    from src.infra.db.models.karaoke import Karaoke
    from src.infra.db.models.rating import Rating


class Registration(BaseIdTimeStampModel, GuildIdMixin, UserIdMixin):
    """Registration of a user in karaoke session."""

    karaoke_id: Mapped[int] = mapped_column(
        ForeignKey("karaoke.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    song_title: Mapped[str] = mapped_column(String(255), nullable=False)
    song_artist: Mapped[str | None] = mapped_column(String(255), nullable=True)

    karaoke: Mapped["Karaoke"] = relationship(back_populates="registrations")
    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="registration",
        cascade="all, delete-orphan",
    )

    __table_args__ = (Index("ix_registration_user_id", "user_id"),)
