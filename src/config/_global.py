"""The module provides a global config for composing all configs and convenient use throughout the project."""  # noqa: E501

from functools import cached_property

from src.bot.config import Config as BotConfig


class Config:
    """Global config for composing all configs and convenient use throughout the project."""  # noqa: E501

    @cached_property
    def bot(self) -> BotConfig:
        """Return the bot configuration settings."""
        return BotConfig()  # type: ignore[call-arg]


config = Config()
