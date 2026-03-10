"""Modal interaction handlers for the karaoke feature."""

from typing import TYPE_CHECKING, cast

from discord import Guild, Interaction

from src.bot.components.embed import ErrorEmbed, SuccessEmbed
from src.infra.db.operations import (
    create_karaoke_registration,
    get_karaoke_by_id,
)

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


async def handle_registration_modal_submit(
    interaction: Interaction["NightcoreKaraoke"],
    karaoke_id: int,
):
    """Handle the registration modal submit button interaction."""

    await interaction.response.defer(ephemeral=True)

    guild = cast(Guild, interaction.guild)

    song_artist = cast(
        str,
        interaction.data["components"][0]["components"][0]["value"],  # type: ignore
    )
    song_title = cast(
        str,
        interaction.data["components"][1]["components"][0]["value"],  # type: ignore
    )

    async with interaction.client.uow.start() as session:
        karaoke = await get_karaoke_by_id(session, karaoke_id)

        if karaoke is None:
            outcome = "not_found"
        else:
            await create_karaoke_registration(
                session,
                guild_id=guild.id,
                karaoke_id=karaoke_id,
                user_id=interaction.user.id,
                song_artist=song_artist,
                song_title=song_title,
            )

            outcome = "success"

    if outcome == "not_found":
        return await interaction.followup.send(
            embed=ErrorEmbed(
                error_message="Караоке не найдено. Пожалуйста, попробуйте снова позже.",  # noqa: E501
                bot=interaction.client,
            ),
            ephemeral=True,
        )

    if outcome == "success":
        return await interaction.followup.send(
            embed=SuccessEmbed(
                interaction.client, "Вы успешно зарегистрировали песню!"
            ),
            ephemeral=True,
        )
