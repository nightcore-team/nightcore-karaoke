"""Karaoke V2 view component."""

from discord import Color
from discord.ui import (
    Container,
    LayoutView,
    TextDisplay,
)


class KaraokeRegistrationView(LayoutView):
    def __init__(self, state: str, message_link: str) -> None:
        super().__init__()

        """Build the karaoke registration view layout."""

        container = Container["KaraokeRegistrationView"](
            accent_color=Color.from_str("#fdcdc9")
        )
        container.add_item(
            TextDisplay(
                f"### <:cat:1480907224523210752> Регистрация на [караоке]({message_link}) {state.lower()}!!!"  # noqa: E501
            )
        )

        self.add_item(container)
