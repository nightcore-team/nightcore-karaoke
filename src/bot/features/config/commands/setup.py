"""Karaoke configuration setup command."""

import logging
from typing import TYPE_CHECKING, cast

from discord import Color, Guild, Role, app_commands
from discord.embeds import Embed
from discord.interactions import Interaction

from src.bot.components.embed import NoOptionsSuppliedEmbed
from src.bot.decorators.permissions import (
    PermissionFlagEnum,
    check_required_permissions,
)
from src.bot.features.config._group import config as config_group
from src.bot.features.config.utils.validator import (
    FieldSpec,
    apply_field_changes,
    format_changes,
    int_id_value,
    split_changes,
)
from src.infra.db.models import GuildKaraokeConfig
from src.infra.db.operations import get_karaoke_config

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke

logger = logging.getLogger(__name__)


@config_group.command(name="setup", description="Настроить систему караоке.")  # type: ignore
@app_commands.describe(
    karaoke_host_role_id="Роль ведущего караоке. Укажите ID роли.",
    karaoke_judge_role_id="Роль судьи караоке. Укажите ID роли.",
)
@app_commands.rename(
    karaoke_host_role_id="роль_ведущего",
    karaoke_judge_role_id="роль_судьи",
)  # type: ignore
@check_required_permissions(PermissionFlagEnum.KARAOKE_CONFIG_ACCESS)
async def setup(
    interaction: Interaction["NightcoreKaraoke"],
    karaoke_host_role_id: Role | None = None,
    karaoke_judge_role_id: Role | None = None,
):
    """Configure karaoke settings."""

    guild = cast(Guild, interaction.guild)

    specs: list[FieldSpec | None] = [
        int_id_value("karaoke_host_role_id", karaoke_host_role_id),
        int_id_value("karaoke_judge_role_id", karaoke_judge_role_id),
    ]

    specs = [s for s in specs if s is not None]

    if not specs:
        logger.info(
            "[command] - invoked user=%s guild=%s no_options_supplied",
            interaction.user.id,
            cast(Guild, interaction.guild).id,
        )
        return await interaction.response.send_message(
            embed=NoOptionsSuppliedEmbed(interaction.client),
            ephemeral=True,
        )

    async with interaction.client.uow.start() as session:
        karaoke_config = await get_karaoke_config(session, guild_id=guild.id)
        if not karaoke_config:
            karaoke_config = GuildKaraokeConfig(guild_id=guild.id)
            session.add(karaoke_config)
            await session.flush()

        changes = apply_field_changes(karaoke_config, specs)

    changed, skipped = split_changes(changes)
    description = format_changes(changed, skipped)

    await interaction.response.send_message(
        embed=Embed(
            title="Настройка системы караоке",
            description=description,
            color=Color.green(),
        ),
        ephemeral=True,
    )

    logger.info(
        "[command] - invoked user=%s guild=%s updated=%s skipped=%s",
        interaction.user.id,
        cast(Guild, interaction.guild).id,
        changed,
        skipped,
    )
