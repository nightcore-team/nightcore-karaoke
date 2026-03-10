"""Global handlers for karaoke."""

from typing import TYPE_CHECKING

from discord import Interaction

from .button import handle_participants_button, handle_registration_button
from .modal import handle_registration_modal_submit

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


async def global_karaoke_handler(
    interaction: Interaction["NightcoreKaraoke"], custom_id: str
):
    """Handle global karaoke interactions."""

    custom_id_parts = custom_id.split(":")

    if len(custom_id_parts) == 3:
        _, category, karaoke_id = custom_id_parts

        if karaoke_id.isdigit():
            match category:
                case "participants":
                    await handle_participants_button(
                        interaction, int(karaoke_id)
                    )

                case "register":
                    await handle_registration_button(
                        interaction, int(karaoke_id)
                    )

                case "register_modal":
                    await handle_registration_modal_submit(
                        interaction, int(karaoke_id)
                    )

                case _:
                    ...
