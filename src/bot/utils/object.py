"""Discord-related object utilities."""

import logging
from typing import TYPE_CHECKING, cast

from discord import Guild, Message, Thread
from discord.abc import GuildChannel, Messageable
from discord.errors import HTTPException, NotFound

if TYPE_CHECKING:
    from discord import Guild, Role

    from src.bot.client import NightcoreKaraoke

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


async def ensure_messageable_channel_exists(
    guild: Guild, channel_id: int
) -> GuildChannel | Thread | None:
    """Ensure that a channel with the given ID exists in the guild and is messageable."""  # noqa: E501

    channel = guild.get_channel(channel_id)
    if channel is None:
        try:
            channel = await guild.fetch_channel(channel_id)  # type: ignore
            if not isinstance(channel, Messageable):
                logger.info(
                    "[ensure_messageable_channel_exists] channel %s not messageable (%s)",  # noqa: E501
                    channel.id,  # type: ignore
                    type(channel).__name__,
                )
                return None
        except NotFound as e:
            logger.info(
                "[ensure_messageable_channel_exists] Channel %s not found in guild %s: %s",  # noqa: E501
                channel_id,
                guild.id,
                e,
            )
            return None
        except HTTPException as e:
            logger.error(
                "[ensure_messageable_channel_exists] Failed refetching channel %s in guild %s: %s",  # noqa: E501
                channel_id,
                guild.id,
                e,
            )
            return None

    return channel


async def ensure_message_exists(
    bot: "NightcoreKaraoke", channel: GuildChannel | Thread, message_id: int
) -> Message | None:
    """Ensure that a message with the given ID exists in the channel."""

    cached = next((m for m in bot.cached_messages if m.id == message_id), None)
    if cached is not None:
        return cached

    try:
        message = await channel.fetch_message(message_id)  # type: ignore
    except NotFound as e:
        logger.error(
            "[ensure_message_exists] Message %s not found in channel %s: %s",
            message_id,
            channel.id,  # type: ignore
            e,
        )
        return None
    except HTTPException as e:
        logger.error(
            "[ensure_message_exists] Failed fetching message %s in channel %s: %s",  # noqa: E501
            message_id,
            channel.id,  # type: ignore
            e,
        )
        return None

    return message  # type: ignore


def cast_guild(value: object) -> Guild:
    """Cast a value to a Guild, if possible."""
    return cast(Guild, value)


def cast_message(value: object) -> Message:
    """Cast a value to a Message, if possible."""
    return cast(Message, value)
