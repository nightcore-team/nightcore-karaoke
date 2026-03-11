"""Karaoke end V2 view component."""

from discord import Color
from discord.ui import (
    Container,
    LayoutView,
    Separator,
    TextDisplay,
)


class KaraokeEndView(LayoutView):
    def __init__(
        self, total_registrations: int, host_id: int, message_link: str
    ) -> None:
        super().__init__()

        """Build the karaoke end view layout."""

        container = Container["KaraokeEndView"](
            accent_color=Color.from_str("#fdcdc9")
        )
        container.add_item(
            TextDisplay(
                f"### <:microphone:1480906998689300491> [Караоке]({message_link}) было завершено!\n"  # noqa: E501
                f"> Общее количество участников: {total_registrations}\n"
                "> Спасибо всем за участие и до новых встреч! <:cat:1480907224523210752>",  # noqa: E501
            )
        )
        container.add_item(Separator())

        container.add_item(
            TextDisplay(
                f"### <:cat:1480907224523210752> Организатор: <@{host_id}>"  # noqa: E501)  # noqa: E501
            )
        )

        self.add_item(container)
