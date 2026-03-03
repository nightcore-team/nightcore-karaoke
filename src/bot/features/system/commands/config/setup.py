"""Subcommands to setup access to each system."""

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
from src.bot.features.config.utils.validator import (
    FieldSpec,
    apply_field_changes,
    format_changes,
    list_csv_value,
    split_changes,
    update_id_list,
)
from src.bot.features.system._group import system as system_group
from src.infra.db.models import GuildPermissionsConfig
from src.infra.db.operations import get_permissions_config

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke

logger = logging.getLogger(__name__)


@system_group.command(
    name="setup_access", description="Настроить доступ к указанной системе."
)  # type: ignore
@app_commands.describe(
    karaoke="Список ролей с доступом к настройке системы караоке. Формат: role_id,role_id,...",  # noqa: E501
)
@app_commands.rename(karaoke="караоке")
@check_required_permissions(PermissionFlagEnum.BOT_ACCESS)
async def setup_access(
    interaction: Interaction["NightcoreKaraoke"],
    karaoke: str | None = None,
):
    """Configure system access settings."""

    guild = cast(Guild, interaction.guild)

    specs: list[FieldSpec | None] = [
        list_csv_value("karaoke_config_access_roles_ids", karaoke),
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
        karaoke_config = await get_permissions_config(
            session, guild_id=guild.id
        )
        changes = apply_field_changes(karaoke_config, specs)

    changed, skipped = split_changes(changes)
    description = format_changes(changed, skipped)

    await interaction.response.send_message(
        embed=Embed(
            title="Настройка доступа к системе",
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


@system_group.command(
    name="update_access",
    description="Обновить список ролей с доступом к указанной системе",
)  # type: ignore
@app_commands.choices(
    system=[
        app_commands.Choice(name="Караоке", value="karaoke"),
    ],
    option=[
        app_commands.Choice(name="Добавить", value="add"),
        app_commands.Choice(name="Удалить", value="remove"),
    ],
)
@app_commands.describe(
    system="Система для обновления доступа",
    role="Роль для обновления",
    option="Добавить или удалить роль из списка доступа",
)
@app_commands.rename(system="система", role="роль", option="опция")
@check_required_permissions(PermissionFlagEnum.BOT_ACCESS)
async def update_config_access(
    interaction: Interaction["NightcoreKaraoke"],
    system: app_commands.Choice[str],
    role: Role,
    option: str,
):
    """Update the list of roles with config access."""

    guild = cast(Guild, interaction.guild)
    state = ""

    async with interaction.client.uow.start() as session:
        guild_config = await get_permissions_config(session, guild_id=guild.id)
        if not guild_config:
            guild_config = GuildPermissionsConfig(guild_id=guild.id)
            session.add(guild_config)
            await session.flush()

        new_list, changed, state = update_id_list(
            guild_config.karaoke_config_access_roles_ids,
            role.id,
            option,
        )
        if changed:
            guild_config.karaoke_config_access_roles_ids = new_list

    if state == "exists":
        desc = f"Роль <@&{role.id}> уже в списке доступа."
        color = Color.yellow()
    elif state == "absent":
        desc = f"Роль <@&{role.id}> не в списке доступа."
        color = Color.red()
    elif state == "added":
        desc = f"Роль <@&{role.id}> добавлена в список доступа{'ко всем системам' if system.value == 'all' else ''}."  # noqa: E501
        color = Color.blurple()
    else:  # removed
        desc = f"Роль <@&{role.id}> удалена из списка доступа{'всех систем' if system.value == 'all' else ''}."  # noqa: E501
        color = Color.blurple()

    await interaction.response.send_message(
        embed=Embed(
            title="Настройка доступа к системе",
            description=desc,
            color=color,
        ),
        ephemeral=True,
    )

    logger.info(
        "[command] - invoked user=%s guild=%s option=%s role=%s system=%s",
        interaction.user.id,
        cast(Guild, interaction.guild).id,
        option,
        role.id,
        system.value,
    )
