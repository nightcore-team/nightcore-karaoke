"""Setup module for creating and configuring bot instance.

To enable/disable features, comment out or remove them from the
ENABLED_FEATURES list.
"""

from src.bot.client import CustomBot
from src.bot.events import get_cogs as get_event_cogs
from src.bot.features.meta.setup import get_cogs as get_meta_cogs
from src.bot.tasks import get_cogs as get_task_cogs


def create_bot() -> CustomBot:
    """Create and return an instance of the CustomBot."""

    # ============================================
    # FEATURE CONFIGURATION
    # ============================================
    # To disable a feature, comment it out or set to False
    enabled_features = {
        "meta": True,  # Core commands (ping, info, etc.)
        # Add more features here as you create them
        # "moderation": True,
        # "music": True,
        # "economy": True,
    }

    # ============================================
    # COG CONFIGURATION
    # ============================================
    # To disable specific cog categories, comment them out
    enabled_cog_categories = {
        "events": True,  # Event listeners
        "components": True,  # Button/Select menu components
        "tasks": True,  # Background tasks
    }

    # ============================================
    # COLLECT ALL COGS
    # ============================================
    cog_modules: list[str] = []

    # Load feature cogs
    if enabled_features.get("meta", False):
        cog_modules.extend(get_meta_cogs())

    # Add more features here
    # if enabled_features.get("moderation", False):
    #     from src.bot.features.moderation.setup import (
    #         get_cogs as get_moderation_cogs
    #     )
    #     cog_modules.extend(get_moderation_cogs())

    # Load other cog categories
    if enabled_cog_categories.get("events", False):
        cog_modules.extend(get_event_cogs())

    if enabled_cog_categories.get("tasks", False):
        cog_modules.extend(get_task_cogs())

    return CustomBot(cog_modules=cog_modules)
