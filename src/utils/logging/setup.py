"""Setup logging utilities for the application."""

import logging
import sys

import colorlog

from src.utils.logging.config import (
    COLOR_FORMATTER,
    DEFAULT_LOGGING_LEVEL_DICT,
)


def setup_logging() -> tuple[logging.Logger, logging.Logger]:
    """Set up and configure logging for the entire application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO))

    # --- Console handler ---
    console_handler = colorlog.StreamHandler(sys.stdout)
    console_handler.setLevel(
        DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO)
    )
    console_handler.setFormatter(COLOR_FORMATTER)
    root_logger.handlers = [console_handler]

    # --- Discord ---
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(
        DEFAULT_LOGGING_LEVEL_DICT.get("discord", logging.INFO)
    )
    discord_logger.propagate = True

    return (
        root_logger,
        discord_logger,
    )
