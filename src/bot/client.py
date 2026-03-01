"""Nightcore Bot."""

import contextlib
import logging
import time
from datetime import datetime, timezone

import discord
from aiohttp import TCPConnector
from discord import app_commands
from discord.ext.commands import Bot

from src.bot.utils.log.on_ready_log import log_tree_summary

logger = logging.getLogger(__name__)


class GuildOnlyTree(app_commands.CommandTree):
    """Custom CommandTree that checks if the interaction is from a guild before processing commands."""  # noqa: E501

    async def interaction_check(
        self, interaction: discord.Interaction
    ) -> bool:
        """Check if the interaction is from a guild."""
        if interaction.guild is None:
            with contextlib.suppress(discord.InteractionResponded):
                await interaction.response.send_message(
                    "Commands are only available in servers.",
                    ephemeral=True,
                )
            return False
        return True


class CustomBot(Bot):
    """Custom bot class that extends discord.ext.commands.Bot with additional functionality."""  # noqa: E501

    def __init__(
        self,
        *,
        cog_modules: list[str],
    ):
        self.cog_modules = cog_modules

        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            help_command=None,
            tree_cls=GuildOnlyTree,
        )
        self.startup_time: datetime = datetime.now(timezone.utc)

    @property
    def _http_connector(self) -> TCPConnector:
        return TCPConnector(
            limit=100,  # max 100 connections
            ttl_dns_cache=300,  # Cache DNS for 5 minutes
            enable_cleanup_closed=True,
            force_close=False,  # Don't close connection after each request  # noqa: E501
            keepalive_timeout=60,  # Keep connection alive for 60 seconds
        )

    async def load_extensions(self) -> None:
        """Load all bot extensions (cogs)."""
        logger.info("Starting to load extensions...")

        if self.cog_modules:
            for module in self.cog_modules:
                try:
                    logger.info(f"Loading cog: {module}")
                    await self.load_extension(module)
                    logger.info(f"[success] Successfully loaded {module}")
                except Exception as e:
                    logger.error(f"[failed] Failed to load {module}: {e}")
        else:
            logger.warning("No cogs to load")

    async def setup_hook(self) -> None:
        """Setup hook called when the bot is ready to start."""
        logger.info("Setup hook started...")

        await self.load_extensions()

        start = time.perf_counter()
        self.http.connector = self._http_connector
        await self.http.get_bot_gateway()
        end = time.perf_counter()
        logger.info(
            f"[gateway] Fetched bot gateway in {(end - start) * 1000:.2f}ms"
        )

        try:
            logger.info("Starting command sync...")
            synced = await self.tree.sync()
            logger.info(
                f"[success] Successfully synced {len(synced)} commands"
            )

        except Exception as e:
            logger.error(f"[failed] Sync failed: {e}")
            import traceback

            logger.error(traceback.format_exc())

        log_tree_summary(self.tree, logger=logger)

    async def on_ready(self) -> None:
        """Event called when the bot is ready."""
        logger.info(f"Loaded cogs: {list(self.cogs.keys())}")
        logger.info(f"Connected to {len(self.guilds)} guilds")
        logger.info("🚀 Bot started successfully!")
