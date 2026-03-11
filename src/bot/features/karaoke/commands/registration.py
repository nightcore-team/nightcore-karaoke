"""Set staff command."""

import asyncio
import logging
from typing import TYPE_CHECKING, cast

from discord import Guild, Interaction, app_commands

from src.bot.components.embed import ErrorEmbed, SuccessEmbed
from src.bot.decorators.permissions import (
    PermissionFlagEnum,
    check_required_permissions,
)
from src.bot.features.karaoke.components import (
    KaraokeRegistrationView,
    KaraokeView,
)
from src.bot.utils.object import (
    ensure_message_exists,
    ensure_messageable_channel_exists,
)
from src.infra.db.enums import KaraokeRegistrationStateEnum, KaraokeStateEnum
from src.infra.db.operations import get_karaoke_by_guild_id
from src.infra.db.utils import cast_karaoke_model

from .._group import registration as registration_group

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


logger = logging.getLogger(__name__)


@registration_group.command(
    name="status",
    description="Изменить статус регистрации караоке.",
)  # type: ignore
@app_commands.choices(
    status=[
        app_commands.Choice(
            name="Открыта",
            value=KaraokeRegistrationStateEnum.OPEN.value,
        ),
        app_commands.Choice(
            name="Закрыта",
            value=KaraokeRegistrationStateEnum.CLOSED.value,
        ),
    ]
)
@check_required_permissions(PermissionFlagEnum.HOST_ACCESS)  # type: ignore
async def announce(
    interaction: Interaction["NightcoreKaraoke"],
    status: str,
):
    """Announce karaoke command."""

    guild = cast(Guild, interaction.guild)

    outcome = ""
    async with interaction.client.uow.start() as session:
        karaoke = await get_karaoke_by_guild_id(session, guild.id)

        if not karaoke:
            outcome = "karaoke_not_found"
        else:
            if karaoke.registration_state.value == status:
                outcome = "already_in_desired_state"
            else:
                karaoke_registration_state = KaraokeRegistrationStateEnum(
                    status
                )
                karaoke.registration_state = karaoke_registration_state
                karaoke.state = KaraokeStateEnum.GOING

                outcome = "success"

    if outcome == "karaoke_not_found":
        return await interaction.response.send_message(
            embed=ErrorEmbed(
                error_message="Караоке не найдено. Пожалуйста, объявите караоке перед изменением статуса регистрации.",  # noqa: E501
                bot=interaction.client,
            ),
            ephemeral=True,
        )

    if outcome == "already_in_desired_state":
        return await interaction.response.send_message(
            embed=ErrorEmbed(
                error_message=f"Регистрация уже {status.lower()}.",
                bot=interaction.client,
            ),
            ephemeral=True,
        )

    if outcome == "success":
        response = interaction.response.send_message(
            embed=ErrorEmbed(
                error_message="Канал/сообщение для регистрации не найдено.",
                bot=interaction.client,
            ),
            ephemeral=True,
        )

        if not (karaoke.channel_id and karaoke.channel_id):  # type: ignore
            return await response
        else:
            channel = await ensure_messageable_channel_exists(
                guild,
                karaoke.channel_id,  # type: ignore
            )
            if not channel:
                return await response

            message = await ensure_message_exists(
                interaction.client,
                channel,
                karaoke.message_id,  # type: ignore
            )

            if not message:
                return await response

            _karaoke = cast_karaoke_model(karaoke)

            original_message_view = KaraokeView(
                karaoke_id=_karaoke.id,
                name=_karaoke.name,
                description=_karaoke.description,
                karaoke_state=_karaoke.state.value,
                registration_state=_karaoke.registration_state.value,
                host_id=_karaoke.host_id,
                prizes=_karaoke.prizes,
            ).build(
                disable_buttons=_karaoke.registration_state
                == KaraokeRegistrationStateEnum.CLOSED
            )
            registration_view = KaraokeRegistrationView(
                state=_karaoke.registration_state.value,
                message_link=message.jump_url,
            )

            asyncio.create_task(message.edit(view=original_message_view))
            await channel.send(view=registration_view)  # type: ignore

            await interaction.response.send_message(
                embed=SuccessEmbed(
                    message="Статус регистрации успешно изменён.",
                    bot=interaction.client,
                ),
                ephemeral=True,
            )
