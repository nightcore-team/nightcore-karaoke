"""Guild Configuration Configs."""

from sqlalchemy import ARRAY, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.db.mixins import GuildIdMixin
from src.infra.db.models.base import BaseIdTimeStampModel


class GuildKaraokeConfig(BaseIdTimeStampModel, GuildIdMixin):  #
    """Karaoke configuration for a guild."""

    karaoke_access_roles_ids: Mapped[list[int] | None] = mapped_column(
        ARRAY(BigInteger), nullable=True
    )
    karaoke_host_role_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    karaoke_judge_role_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
