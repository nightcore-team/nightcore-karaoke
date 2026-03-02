"""This file contains mixins for database models."""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )


@declarative_mixin
class IdIntegerMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


@declarative_mixin
class GuildIdMixin:
    guild_id: Mapped[int] = mapped_column(BigInteger, nullable=False)


@declarative_mixin
class UserIdMixin:
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
