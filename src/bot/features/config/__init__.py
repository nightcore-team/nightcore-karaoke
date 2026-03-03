"""Setup module for config feature.

This module collects all cogs from the config feature.
To disable specific cogs, modify the imports or the COGS list below.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke

from ._group import config as config_group

# SIDE-EFFECT IMPORTS
from .commands import setup as setup_command

__all__ = ("setup_command",)

COGS = [
    "src.bot.features.config",
]


def get_cogs() -> list[str]:
    """Return list of all enabled cog modules in the config feature."""
    return COGS


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup the clans commands for the Nightcore bot."""
    bot.tree.add_command(config_group)
