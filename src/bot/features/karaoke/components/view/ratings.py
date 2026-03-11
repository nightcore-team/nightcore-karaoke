"""Karaoke end V2 view component."""

from typing import TYPE_CHECKING

from discord import Color
from discord.ui import (
    Container,
    LayoutView,
    Separator,
    TextDisplay,
)

if TYPE_CHECKING:
    from src.infra.db.models import Registration


class KaraokeRatingsView(LayoutView):
    def __init__(
        self,
        karaoke_name: str,
        ratings: list[tuple["Registration", float]],
        karaoke_message_link: str | None = None,
    ) -> None:
        super().__init__()
        """Build the karaoke end view layout."""

        container = Container["KaraokeRatingsView"](
            accent_color=Color.from_str("#fdcdc9")
        )

        karaoke_text = (
            f"Результаты [{karaoke_name}]({karaoke_message_link})\n"
            if karaoke_message_link
            else f"Результаты {karaoke_name}\n"
        )
        container.add_item(
            TextDisplay(
                f"## <:microphone:1480906998689300491> {karaoke_text}"
                f"> Всего оценок: {len(ratings)}\n"
            )
        )
        container.add_item(Separator())

        container.add_item(TextDisplay("### Рейтинг участников:\n"))

        ratings_text = "> Список пуст."
        if ratings:
            ratings_text = "\n".join(
                f"> <:pets:1480954494354194473> <@{registration.user_id}>: {registration.song_artist} - {registration.song_title}: {average_score:.1f}"  # noqa: E501
                for registration, average_score in ratings
            )

        container.add_item(TextDisplay(ratings_text))

        self.add_item(container)
