"""Karaoke commands groups."""

from discord import app_commands

registration = app_commands.Group(
    name="registration",
    description="Команды управления регистрацией на караоке.",
)
