"""Command to check bot latency."""

from typing import TYPE_CHECKING

from discord import app_commands
from discord.ext.commands import Cog
from discord.interactions import Interaction

if TYPE_CHECKING:
    from src.bot.client import CustomBot


class Ping(Cog):
    def __init__(self, bot: "CustomBot") -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: Interaction) -> None:
        """Send a message displaying the bot's current latency."""

        await interaction.response.send_message(
            f"Pong! Latency: {self.bot.latency * 1000:.2f} ms", ephemeral=True
        )


async def setup(bot: "CustomBot") -> None:
    """Setup the Ping cog."""
    await bot.add_cog(Ping(bot))
