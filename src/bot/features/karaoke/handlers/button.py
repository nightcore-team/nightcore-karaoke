"""Button interaction handlers for the karaoke feature."""

from typing import TYPE_CHECKING

from discord import Interaction

from src.bot.components.embed import ErrorEmbed
from src.bot.utils.object import cast_message
from src.infra.db.operations import get_karaoke_by_id, get_karaoke_results
from src.infra.db.utils import cast_karaoke_model

from ..components import (
    KaraokePariticipantsListView,
    KaraokeRatingsView,
    KaraokeRegistrationModal,
)

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


async def handle_participants_button(
    interaction: Interaction["NightcoreKaraoke"], karaoke_id: int
):
    """Handle the participants button interaction."""

    await interaction.response.defer()

    outcome = ""
    participants = []
    async with interaction.client.uow.start() as session:
        karaoke = await get_karaoke_by_id(session, karaoke_id)

        if karaoke is None:
            outcome = "not_found"
        else:
            participants = karaoke.registrations
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
        view = KaraokePariticipantsListView(participants=participants)

        return await interaction.followup.send(view=view, ephemeral=True)


async def handle_registration_button(
    interaction: Interaction["NightcoreKaraoke"], karaoke_id: int
):
    """Handle the registration button interaction."""

    await interaction.response.send_modal(
        KaraokeRegistrationModal(karaoke_id=karaoke_id)
    )


async def handle_results_button(
    interaction: Interaction["NightcoreKaraoke"], karaoke_id: int
):
    """Handle the results button interaction."""

    await interaction.response.defer()

    outcome = ""
    ratings = []
    async with interaction.client.uow.start() as session:
        karaoke = await get_karaoke_by_id(session, karaoke_id)

        if karaoke is None:
            outcome = "not_found"
        else:
            ratings = await get_karaoke_results(session, karaoke_id)
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
        message = cast_message(interaction.message)
        _karaoke = cast_karaoke_model(karaoke)

        view = KaraokeRatingsView(
            karaoke_name=_karaoke.name,
            karaoke_message_link=message.jump_url,
            ratings=ratings,
        )

        return await interaction.followup.send(view=view, ephemeral=True)
