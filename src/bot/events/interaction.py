"""Interaction events module."""

import logging
from typing import TYPE_CHECKING

from discord import Interaction, InteractionType

from src.bot.features.karaoke.handlers import global_karaoke_handler

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke

logger = logging.getLogger(__name__)


def _extract_custom_id(
    interaction: Interaction["NightcoreKaraoke"],
) -> str | None:
    data = interaction.data
    if not isinstance(data, dict):
        return None

    custom_id = data.get("custom_id")
    return custom_id if isinstance(custom_id, str) else None


async def _dispatch_component_interaction(
    interaction: Interaction["NightcoreKaraoke"],
    custom_id: str,
) -> None:

    if custom_id.startswith("karaoke"):
        await global_karaoke_handler(interaction, custom_id)

    logger.info("Unhandled component custom_id: %s", custom_id)


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup interaction events for the Nightcore bot."""

    @bot.event
    async def on_interaction(  # type: ignore
        interaction: Interaction["NightcoreKaraoke"],
    ) -> None:
        """Handle global Discord interactions."""
        custom_id = _extract_custom_id(interaction)

        logger.info(
            "Received interaction type=%s user_id=%s custom_id=%s",
            interaction.type,
            getattr(interaction.user, "id", None),
            custom_id,
        )

        if interaction.type not in [
            InteractionType.component,
            InteractionType.modal_submit,
        ]:
            return

        if custom_id is None:
            logger.info("Component interaction without custom_id")
            return

        await _dispatch_component_interaction(interaction, custom_id)
