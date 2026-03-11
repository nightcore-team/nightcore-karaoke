"""Close karaoke command."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, cast

from discord import Guild, Interaction, app_commands
from discord.ext.commands import Cog  # type: ignore

from src.bot.components.embed import ErrorEmbed, SuccessEmbed
from src.bot.decorators.permissions import (
    PermissionFlagEnum,
    check_required_permissions,
)
from src.bot.features.karaoke.components import KaraokeEndView, KaraokeView
from src.bot.utils.object import (
    ensure_message_exists,
    ensure_messageable_channel_exists,
)
from src.infra.db.enums import KaraokeRegistrationStateEnum, KaraokeStateEnum
from src.infra.db.operations import (
    get_karaoke_by_guild_id,
)
from src.infra.db.utils import cast_karaoke_model

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


logger = logging.getLogger(__name__)


class Close(Cog):
    def __init__(self) -> None:
        super().__init__()

    @app_commands.command(
        name="close",
        description="Закрыть текущее караоке.",
    )  # type: ignore
    @check_required_permissions(PermissionFlagEnum.HOST_ACCESS)  # type: ignore
    async def close(
        self,
        interaction: Interaction["NightcoreKaraoke"],
    ):
        """Close karaoke command."""

        guild = cast(Guild, interaction.guild)

        outcome = ""
        total_participants = 0
        async with interaction.client.uow.start() as session:
            karaoke = await get_karaoke_by_guild_id(
                session, guild.id, with_registrations=True
            )

            if karaoke is None:
                outcome = "not_found"
            else:
                karaoke.registration_state = (
                    KaraokeRegistrationStateEnum.CLOSED
                )
                karaoke.state = KaraokeStateEnum.FINISHED
                karaoke.end_time = datetime.now(timezone.utc)

                total_participants = len(karaoke.registrations)

                outcome = "success"

        if outcome == "not_found":
            return await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message="Караоке не найдено в этом сервере. Пожалуйста, убедитесь, что караоке было объявлено перед его закрытием.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )

        if outcome == "success":
            response = interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message="Канал/сообщение с караоке не найдено.",
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
            end_view = KaraokeEndView(
                total_registrations=total_participants,
                host_id=_karaoke.host_id,
                message_link=message.jump_url,
            )

            asyncio.create_task(message.edit(view=original_message_view))
            await channel.send(view=end_view)  # type: ignore

            await interaction.response.send_message(
                embed=SuccessEmbed(
                    message="Караоке успешно закрыто!",
                    bot=interaction.client,
                ),
                ephemeral=True,
            )


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup function for the close command."""
    await bot.add_cog(Close())
