"""Configuration commands groups."""

from discord import app_commands

config = app_commands.Group(
    name="config", description="Команды настройки системы караоке."
)
