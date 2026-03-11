"""Autocomplete utilities for karaoke features."""

import contextlib
import logging
from typing import TYPE_CHECKING, cast

from discord import Guild, Interaction, app_commands

from src.infra.db.operations import get_karaoke_by_guild_id

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


logger = logging.getLogger(__name__)


async def vote_registration_autocomplete(
    interaction: Interaction["NightcoreKaraoke"],
    current: str,
) -> list[app_commands.Choice[str]]:
    """
    Autocomplete for selecting a registration (song) for a specific user in a vote.

    This function demonstrates how to use the value of one argument ('user')
    to filter the choices of another argument ('registration_id').
    """  # noqa: E501
    guild = cast(Guild, interaction.guild)
    if not guild:
        return []

    selected_user = getattr(interaction.namespace, "участник", None)
    selected_user_id: int | None = None

    if selected_user is not None:
        if hasattr(selected_user, "id"):
            selected_user_id = selected_user.id
        else:
            with contextlib.suppress(ValueError, TypeError):
                selected_user_id = int(selected_user)

    if selected_user_id is None:
        return [
            app_commands.Choice(
                name="Сначала выберите участника",
                value="error_no_user",
            )
        ]

    choices: list[app_commands.Choice[str]] = []

    async with interaction.client.uow.start() as session:
        karaoke = await get_karaoke_by_guild_id(
            session, guild.id, with_registrations=True
        )

        if karaoke and karaoke.registrations:
            # Filter registrations by user_id
            user_registrations = [
                reg
                for reg in karaoke.registrations
                if reg.user_id == selected_user_id
            ]

            # Filter by current search string
            filtered_registrations = [
                reg
                for reg in user_registrations
                if current.lower()
                in f"{reg.song_artist} - {reg.song_title}".lower()
            ]

            for reg in filtered_registrations[:25]:
                display_name = f"{reg.song_artist} - {reg.song_title}"
                if len(display_name) > 100:
                    display_name = display_name[:97] + "..."

                choices.append(
                    app_commands.Choice(name=display_name, value=str(reg.id))
                )

    if not choices:
        return [
            app_commands.Choice(
                name="У этого участника нет активных регистраций",
                value="error_no_registrations",
            )
        ]

    return choices
