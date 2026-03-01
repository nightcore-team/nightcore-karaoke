"""Meta commands package.

Contains all command cogs for the meta feature.
"""

# List of all cog modules in this package
# To disable a specific cog, comment it out or remove it from this list
from typing import Final

COGS: Final[list[str]] = [
    "src.bot.features.meta.commands.ping",
]


def get_cogs() -> list[str]:
    """Return list of enabled cog modules in this package."""
    return COGS
