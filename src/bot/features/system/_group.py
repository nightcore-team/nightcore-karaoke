"""System configuration commands group."""

from discord import app_commands

system = app_commands.Group(
    name="system",
    description="Команды настройки системных параметров.",
)
