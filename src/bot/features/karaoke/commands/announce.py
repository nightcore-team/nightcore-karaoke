"""Set staff command."""

import logging
from typing import TYPE_CHECKING, cast

from discord import Guild, Interaction, TextChannel, app_commands
from discord.ext.commands import Cog  # type: ignore

from src.bot.components.embed import ErrorEmbed, SuccessEmbed
from src.bot.decorators.permissions import (
    PermissionFlagEnum,
    check_required_permissions,
)
from src.bot.features.karaoke.components import KaraokeView
from src.infra.db.enums import KaraokeRegistrationStateEnum, KaraokeStateEnum
from src.infra.db.operations import (
    create_karaoke,
    get_karaoke_by_guild_id,
)

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


logger = logging.getLogger(__name__)


class Announce(Cog):
    def __init__(self) -> None:
        super().__init__()

    @app_commands.command(
        name="announce",
        description="Объявить новое караоке.",
    )  # type: ignore
    @check_required_permissions(PermissionFlagEnum.HOST_ACCESS)  # type: ignore
    async def announce(
        self,
        interaction: Interaction["NightcoreKaraoke"],
        name: app_commands.Range[str, 1, 100],
        description: app_commands.Range[str, 1, 1000] | None = None,
        prizes: app_commands.Range[str, 1, 1000] | None = None,
    ):
        """Announce karaoke command."""

        guild = cast(Guild, interaction.guild)

        _prizes: list[str] | None = None
        try:
            _prizes = (
                [prize.strip() for prize in prizes.split("|")]
                if prizes
                else None
            )
        except Exception as e:
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message=f"Неверный формат для призов. Пожалуйста, используйте разделитель '|'. Ошибка: {e!s}",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )
            logger.error("Invalid format for prizes: %s", e)

        outcome = ""
        async with interaction.client.uow.start() as session:
            karaoke = await get_karaoke_by_guild_id(session, guild.id)

            if karaoke:
                outcome = "already_announced"
            else:
                karaoke = await create_karaoke(
                    session,
                    guild.id,
                    interaction.user.id,
                    name,
                    description,
                    _prizes,
                )

                outcome = "success"

                await session.flush()

        if outcome == "already_announced":
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message="В этом сервере уже есть объявленное караоке. Завершите его, прежде чем объявлять новое.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )

        if outcome == "success":
            view = KaraokeView(
                karaoke_id=karaoke.id,
                name=name,
                description=description,
                prizes=_prizes,
                karaoke_state=KaraokeStateEnum.ANNOUNCED.value,
                registration_state=KaraokeRegistrationStateEnum.CLOSED.value,
                host_id=interaction.user.id,
            )

            try:
                await interaction.channel.send(f"<@&{guild.default_role.id}>")  # type: ignore
                message = await cast(TextChannel, interaction.channel).send(
                    view=view.build()
                )

            except Exception as e:
                await interaction.response.send_message(
                    embed=ErrorEmbed(
                        error_message=f"Не удалось отправить сообщение с анонсом караоке. Пожалуйста, убедитесь, что у бота есть разрешение на отправку сообщений в этом канале. Ошибка: {e!s}",  # noqa: E501
                        bot=interaction.client,
                    ),
                    ephemeral=True,
                )
                logger.error(
                    "Failed to send karaoke announcement message: %s", e
                )
                return

            async with interaction.client.uow.start() as session:
                karaoke = await session.merge(karaoke)
                karaoke.message_id = message.id
                karaoke.channel_id = message.channel.id

            return await interaction.response.send_message(
                embed=SuccessEmbed(
                    message="Караоке успешно объявлено!",
                    bot=interaction.client,
                ),
                ephemeral=True,
            )


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup function for the announce command."""
    await bot.add_cog(Announce())
