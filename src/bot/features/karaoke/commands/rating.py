"""Karaoke rating command."""

import logging
from typing import TYPE_CHECKING

from discord import Interaction, app_commands
from discord.ext.commands import Cog  # type: ignore

from src.bot.components.embed import ErrorEmbed
from src.bot.decorators.permissions import (
    PermissionFlagEnum,
    check_required_permissions,
)
from src.bot.features.karaoke.components import KaraokeRatingsView
from src.bot.features.karaoke.utils.autocomplete import karaoke_autocomplete
from src.bot.utils.object import (
    cast_guild,
    ensure_message_exists,
    ensure_messageable_channel_exists,
)
from src.infra.db.operations import (
    get_karaoke_by_id,
    get_karaoke_results,
)
from src.infra.db.utils import cast_karaoke_model

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


logger = logging.getLogger(__name__)


class Rating(Cog):
    def __init__(self) -> None:
        super().__init__()

    @app_commands.command(
        name="rating",
        description="Показать рейтинг участников выбранного караоке.",
    )  # type: ignore
    @check_required_permissions(PermissionFlagEnum.NONE)  # type: ignore
    @app_commands.autocomplete(karaoke_id=karaoke_autocomplete)
    @app_commands.rename(karaoke_id="караоке")
    async def rating(
        self,
        interaction: Interaction["NightcoreKaraoke"],
        karaoke_id: str,
    ):
        """Show karaoke rating command."""

        guild = cast_guild(interaction.guild)

        try:
            karaoke_id_int = int(karaoke_id)
        except ValueError:
            return await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message="Некорректный ID караоке. Пожалуйста, выберите караоке из списка.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )

        outcome = ""
        ratings = []
        async with interaction.client.uow.start() as session:
            karaoke = await get_karaoke_by_id(session, karaoke_id_int)

            if karaoke is None:
                outcome = "not_found"
            else:
                ratings = await get_karaoke_results(session, karaoke.id)
                outcome = "success"

        if outcome == "not_found":
            return await interaction.response.send_message(
                embed=ErrorEmbed(
                    error_message="Караоке не найдено. Пожалуйста, попробуйте снова позже.",  # noqa: E501
                    bot=interaction.client,
                ),
                ephemeral=True,
            )

        if outcome == "success":
            await interaction.response.defer(ephemeral=True, thinking=True)

            _karaoke = cast_karaoke_model(karaoke)
            karaoke_message_link = None

            if not (karaoke.channel_id and karaoke.channel_id):  # type: ignore
                pass
            else:
                channel = await ensure_messageable_channel_exists(
                    guild,
                    karaoke.channel_id,  # type: ignore
                )
                if not channel:
                    pass
                else:
                    message = await ensure_message_exists(
                        interaction.client,
                        channel,
                        karaoke.message_id,  # type: ignore
                    )

                    if not message:
                        pass
                    else:
                        karaoke_message_link = message.jump_url

            view = KaraokeRatingsView(
                karaoke_name=_karaoke.name,
                karaoke_message_link=karaoke_message_link,
                ratings=ratings,
            )

            return await interaction.followup.send(view=view)


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup function for the rating command."""
    await bot.add_cog(Rating())
