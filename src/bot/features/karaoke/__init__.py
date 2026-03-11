"""Setup module for config feature.

This module collects all cogs from the config feature.
To disable specific cogs, modify the imports or the COGS list below.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke

from ._group import registration as registration_group

# SIDE-EFFECT imports
from .commands import registration

__all__ = ("registration", "registration_group")

COGS = [
    "src.bot.features.karaoke.commands.setstaff",
    "src.bot.features.karaoke.commands.vote",
    "src.bot.features.karaoke.commands.announce",
    "src.bot.features.karaoke.commands.close",
    "src.bot.features.karaoke",
]


def get_cogs() -> list[str]:
    """Return list of all enabled cog modules in the config feature."""
    return COGS


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup the clans commands for the Nightcore bot."""
    bot.tree.add_command(registration_group)
