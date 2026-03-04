"""Discord-related object utilities."""

import logging
from typing import TYPE_CHECKING

from discord.errors import HTTPException, NotFound

if TYPE_CHECKING:
    from discord import Guild, Role

logger = logging.getLogger(__name__)


async def ensure_role_exists(guild: "Guild", role_id: int) -> "Role | None":
    """Ensure that a role with the given ID exists in the guild."""
    role = guild.get_role(role_id)
    if role is None:
        try:
            role = await guild.fetch_role(role_id)
        except NotFound as e:
            logger.error(
                "[ensure_role_exists] Role %s not found in guild %s: %s",
                role_id,
                guild.id,
                e,
            )
            return None
        except HTTPException as e:
            logger.error(
                "[ensure_role_exists] Failed refetching role %s in guild %s: %s",  # noqa: E501
                role_id,
                guild.id,
                e,
            )
            return None

    return role
