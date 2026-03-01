"""Defines the Config class for bot environment settings."""

from src.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Configuration class for bot environment settings."""

    BOT_TOKEN: str
