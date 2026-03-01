"""Setup module for meta feature.

This module collects all cogs from the meta feature.
To disable specific cogs, modify the imports or the COGS list below.
"""

from src.bot.features.meta.commands import get_cogs as get_command_cogs

# Collect all cogs from different categories
COGS = [
    *get_command_cogs(),
    # Add other categories here (events, components, etc.)
]


def get_cogs() -> list[str]:
    """Return list of all enabled cog modules in the meta feature."""
    return COGS
