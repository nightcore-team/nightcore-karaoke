"""Defines the Config class for bot environment settings."""

from typing import Final

from src.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Configuration class for bot environment settings."""

    BOT_TOKEN: str
    DEVELOPERS_IDS: Final[list[int]] = [
        566255833684508672,
        1280700292530176131,
    ]
