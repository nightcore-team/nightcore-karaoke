"""Error event handlers."""

import logging
from typing import TYPE_CHECKING

from discord.app_commands import AppCommandError, MissingPermissions
from discord.errors import RateLimited
from discord.interactions import Interaction

from src.bot.components.embed import ErrorEmbed

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke

logger = logging.getLogger(__name__)


async def on_app_command_error(
    interaction: Interaction["NightcoreKaraoke"],
    error: AppCommandError,
):
    """Handle errors for application commands."""

    original = getattr(error, "original", error)

    if isinstance(original, RateLimited):
        logger.warning(
            "%s handled guild=%s user=%s",
            original.__class__.__name__,
            interaction.guild.id if interaction.guild else "DM",
            interaction.user.id,
        )
        if not interaction.response.is_done():
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message=f"Ошибка при обработке команды: слишком много запросов. Пожалуйста, попробуйте снова через: {original.retry_after} секунд.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message=f"Ошибка при обработке команды: слишком много запросов. Пожалуйста, попробуйте снова через: {original.retry_after} секунд.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )
        return

    if isinstance(original, MissingPermissions):
        logger.warning(
            "%s handled guild=%s user=%s missing_permissions=%s",
            original.__class__.__name__,
            interaction.guild.id if interaction.guild else "DM",
            interaction.user.id,
            original.missing_permissions,
        )
        if not interaction.response.is_done():
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message="У вас недостаточно прав для выполнения этой команды.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message="У вас недостаточно прав для выполнения этой команды.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )
        return


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup function for error event handlers."""
    bot.tree.on_error = on_app_command_error
