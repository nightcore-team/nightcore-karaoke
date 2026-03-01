"""Bot events package.

This package contains all event listener cogs.
To disable a specific event cog, comment it out from the COGS list.
"""

# List of all event cog modules
# To disable a specific event cog, comment it out or remove it from this list
from typing import Final

COGS: Final[list[str]] = [
    # "src.bot.events.on_message",
    # "src.bot.events.on_member_join",
    # "src.bot.events.on_error",
]


def get_cogs() -> list[str]:
    """Return list of enabled event cog modules."""
    return COGS
