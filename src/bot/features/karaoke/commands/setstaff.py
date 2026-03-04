"""Set staff command."""

import asyncio
from typing import TYPE_CHECKING, cast

from discord import Guild, Member, app_commands
from discord.ext.commands import Cog  # type: ignore
from discord.interactions import Interaction

from src.bot.components.embed import ErrorEmbed, SuccessEmbed
from src.bot.decorators.permissions import (
    PermissionFlagEnum,
    check_required_permissions,
)
from src.bot.utils.object import ensure_role_exists
from src.infra.db.enums import KaraokeRoleEnum
from src.infra.db.operations import (
    create_staff,
    delete_staff,
    get_karaoke_config,
    get_karaoke_config_access_roles,
    get_user_staff_role,
    update_staff_role,
)

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


class SetStaff(Cog):
    def __init__(self) -> None:
        super().__init__()

    @app_commands.command(
        name="setstaff",
        description="Назначить пользователя организатором/судьей.",
    )  # type: ignore
    @app_commands.choices(
        role=[
            app_commands.Choice(name="Организатор", value="host"),
            app_commands.Choice(name="Судья", value="judge"),
        ]
    )
    @check_required_permissions(PermissionFlagEnum.UNSAFE)  # type: ignore
    async def set_staff(
        self,
        interaction: Interaction["NightcoreKaraoke"],
        user: Member,
        role: str,
    ):
        """Set staff command."""

        guild = cast(Guild, interaction.guild)

        outcome = ""
        is_remove = False
        previous_user_role: KaraokeRoleEnum | None = None
        async with interaction.client.uow.start() as session:
            user_role = await get_user_staff_role(session, guild.id, user.id)
            previous_user_role = user_role
            karaoke_config = await get_karaoke_config(session, guild.id)

            if role == "host":
                access_roles = await get_karaoke_config_access_roles(
                    session, guild.id
                )
                if access_roles is None:
                    outcome = "no_access_roles_configured"
                elif not any(
                    role.id in access_roles
                    for role in cast(Member, interaction.user).roles
                ):
                    outcome = "missing_permissions"

                if not outcome:
                    if user_role == KaraokeRoleEnum.HOST:
                        await delete_staff(session, guild.id, user.id)
                        is_remove = True
                        outcome = "success"
                    else:
                        if user_role is None:
                            await create_staff(
                                session,
                                guild.id,
                                user.id,
                                KaraokeRoleEnum.HOST,
                            )
                        else:
                            await update_staff_role(
                                session,
                                guild.id,
                                user.id,
                                KaraokeRoleEnum.HOST,
                            )
                        outcome = "success"

            elif role == "judge":
                caller_role = await get_user_staff_role(
                    session, guild.id, interaction.user.id
                )
                if caller_role != KaraokeRoleEnum.HOST:
                    outcome = "missing_permissions"
                else:
                    if user_role == KaraokeRoleEnum.JUDGE:
                        await delete_staff(session, guild.id, user.id)
                        is_remove = True
                        outcome = "success"
                    else:
                        if user_role is None:
                            await create_staff(
                                session,
                                guild.id,
                                user.id,
                                KaraokeRoleEnum.JUDGE,
                            )
                        else:
                            await update_staff_role(
                                session,
                                guild.id,
                                user.id,
                                KaraokeRoleEnum.JUDGE,
                            )
                        outcome = "success"

        if outcome == "no_access_roles_configured":
            return await interaction.response.send_message(
                embed=ErrorEmbed(
                    interaction.client,
                    "Роли доступа не настроены. Пожалуйста, настройте роли доступа и попробуйте снова.",  # noqa: E501
                )
            )

        elif outcome == "missing_permissions":
            raise app_commands.MissingPermissions([])

        elif outcome == "success":
            if karaoke_config:
                role_id = (
                    karaoke_config.karaoke_host_role_id
                    if role == "host"
                    else karaoke_config.karaoke_judge_role_id
                )
                if (
                    role_id is not None
                    and (
                        guild_role := await ensure_role_exists(guild, role_id)
                    )
                    is not None
                ):
                    if is_remove:
                        asyncio.create_task(
                            user.remove_roles(
                                guild_role,
                                reason="Снятие роли персонала караоке",
                            )
                        )  # type: ignore
                    else:
                        asyncio.create_task(
                            user.add_roles(
                                guild_role,
                                reason="Назначение роли персонала караоке",
                            )
                        )  # type: ignore

                if (
                    not is_remove
                    and previous_user_role is not None
                    and previous_user_role
                    != (
                        KaraokeRoleEnum.HOST
                        if role == "host"
                        else KaraokeRoleEnum.JUDGE
                    )
                ):
                    previous_role_id = (
                        karaoke_config.karaoke_host_role_id
                        if previous_user_role == KaraokeRoleEnum.HOST
                        else karaoke_config.karaoke_judge_role_id
                    )
                    if (
                        previous_role_id is not None
                        and (
                            previous_guild_role := await ensure_role_exists(
                                guild, previous_role_id
                            )
                        )
                        is not None
                    ):
                        asyncio.create_task(
                            user.remove_roles(
                                previous_guild_role,
                                reason="Обновление роли персонала караоке",
                            )
                        )  # type: ignore

            message = (
                f"У пользователя {user.mention} снята роль: {role}."
                if is_remove
                else (
                    f"Пользователю {user.mention} "
                    f"успешно назначена роль: {role}."
                )
            )
            return await interaction.response.send_message(
                embed=SuccessEmbed(
                    interaction.client,
                    message,
                ),
            )


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup function for the setstaff command."""
    await bot.add_cog(SetStaff())
