"""Bot tasks package.

This package contains all background task cogs.
To disable a specific task cog, comment it out from the COGS list.
"""

# List of all task cog modules
# To disable a specific task cog, comment it out or remove it from this list
from typing import Final

COGS: Final[list[str]] = [
    # "src.bot.tasks.status_updater",
    # "src.bot.tasks.cleanup_task",
]


def get_cogs() -> list[str]:
    """Return list of enabled task cog modules."""
    return COGS
