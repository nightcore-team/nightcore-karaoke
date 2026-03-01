"""Main entry point for the Nightcore bot."""

from src.bot.setup import create_bot
from src.config._global import config
from src.config.env import ENV_PATH
from src.utils.logging.setup import setup_logging


def main() -> None:
    """Main function to start the Nightcore bot."""
    logger, discord_logger = setup_logging()
    bot = create_bot()

    logger.info("Starting bot...")
    logger.info("Loading environment variables from: %s", ENV_PATH)

    try:
        bot.run(config.bot.BOT_TOKEN, log_handler=discord_logger.handlers[0])
    except Exception as e:
        logger.error("Error occurred: %s", e)
    finally:
        logger.info("Bot has been stopped.")


if __name__ == "__main__":
    main()
