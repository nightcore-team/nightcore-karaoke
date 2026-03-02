"""Rating model."""

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.mixins import GuildIdMixin, UserIdMixin
from src.infra.db.models.base import BaseIdTimeStampModel

if TYPE_CHECKING:
    from src.infra.db.models.karaoke import Karaoke
    from src.infra.db.models.registration import Registration


class Rating(BaseIdTimeStampModel, GuildIdMixin, UserIdMixin):
    """Rating for a participant in a karaoke session."""

    __table_args__ = (
        CheckConstraint("score >= 1 AND score <= 10", name="ck_rating_score"),
    )

    karaoke_id: Mapped[int] = mapped_column(
        ForeignKey("karaoke.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    registration_id: Mapped[int | None] = mapped_column(
        ForeignKey("registration.id", ondelete="SET NULL"),
        nullable=True,
    )
    judge_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    karaoke: Mapped["Karaoke"] = relationship(back_populates="ratings")
    registration: Mapped["Registration | None"] = relationship(
        back_populates="ratings"
    )
