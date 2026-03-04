"""Embed components."""

from typing import TYPE_CHECKING

from discord import Color
from discord.embeds import Embed

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke


class NoOptionsSuppliedEmbed(Embed):
    def __init__(self, bot: "NightcoreKaraoke") -> None:
        super().__init__(
            title="Не предоставлены параметры",
            description="Для этой команды не было предоставлено никаких параметров.",  # noqa: E501
            color=Color.yellow(),
        )
        self.set_footer(
            text=bot.user.name, icon_url=bot.user.display_avatar.url
        )


class ErrorEmbed(Embed):
    def __init__(self, bot: "NightcoreKaraoke", error_message: str) -> None:
        super().__init__(
            title="Ошибка",
            description=error_message,
            color=Color.red(),
        )
        self.set_footer(
            text=bot.user.name, icon_url=bot.user.display_avatar.url
        )


class SuccessEmbed(Embed):
    def __init__(self, bot: "NightcoreKaraoke", message: str) -> None:
        super().__init__(
            title="Успешно",
            description=message,
            color=Color.green(),
        )
        self.set_footer(
            text=bot.user.name, icon_url=bot.user.display_avatar.url
        )
