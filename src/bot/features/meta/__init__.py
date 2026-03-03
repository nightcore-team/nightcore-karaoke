"""Setup module for meta feature.

This module collects all cogs from the meta feature.
To disable specific cogs, modify the imports or the COGS list below.
"""

# Collect all cogs from different categories
COGS = ["src.bot.features.meta.commands.ping"]


def get_cogs() -> list[str]:
    """Return list of all enabled cog modules in the meta feature."""
    return COGS
