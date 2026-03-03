"""Database operations module."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.enums import KaraokeRoleEnum

from .models import GuildKaraokeConfig, GuildPermissionsConfig, Staff


async def get_karaoke_config(
    session: AsyncSession, guild_id: int
) -> GuildKaraokeConfig | None:
    """Fetch the karaoke configuration for a specific guild."""

    result = await session.execute(
        select(GuildKaraokeConfig).where(
            GuildKaraokeConfig.guild_id == guild_id
        )
    )
    return result.scalar_one_or_none()


async def get_permissions_config(
    session: AsyncSession, guild_id: int
) -> GuildPermissionsConfig | None:
    """Fetch the permissions configuration for a specific guild."""

    result = await session.execute(
        select(GuildPermissionsConfig).where(
            GuildPermissionsConfig.guild_id == guild_id
        )
    )
    return result.scalar_one_or_none()


async def get_user_staff_role(
    session: AsyncSession, guild_id: int, user_id: int
) -> KaraokeRoleEnum | None:
    """Fetch the staff role of a user in a specific guild."""

    result = await session.execute(
        select(Staff).where(
            Staff.guild_id == guild_id, Staff.user_id == user_id
        )
    )

    result = result.scalar_one_or_none()
    return result.role if result else None
