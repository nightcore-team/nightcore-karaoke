"""Setup module for config feature.

This module collects all cogs from the config feature.
To disable specific cogs, modify the imports or the COGS list below.
"""

COGS = [
    "src.bot.features.karaoke.commands.setstaff",
]


def get_cogs() -> list[str]:
    """Return list of all enabled cog modules in the config feature."""
    return COGS
