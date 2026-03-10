"""Global handlers for karaoke."""

from typing import TYPE_CHECKING

from discord import Interaction

from .button import handle_participants_button

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


async def global_karaoke_handler(
    interaction: Interaction["NightcoreKaraoke"], custom_id: str
):
    """Handle global karaoke interactions."""

    custom_id_parts = custom_id.split(":")

    if len(custom_id_parts) == 3:
        _, category, karaoke_id = custom_id_parts

        match category:
            case "participants":
                if karaoke_id.isdigit():
                    await handle_participants_button(
                        interaction, int(karaoke_id)
                    )

            case "results":
                ...

            case _:
                ...
