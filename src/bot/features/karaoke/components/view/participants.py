"""Karaoke participants list V2 view component."""

from discord.ui import Container, LayoutView, Separator, TextDisplay

from src.infra.db.models import Registration


class KaraokePariticipantsListView(LayoutView):
    def __init__(self, participants: list[Registration]) -> None:
        super().__init__(timeout=None)

        container = Container["KaraokePariticipantsListView"]()
        container.add_item(
            TextDisplay(
                "## <:group:1480910755493712062> Список участников караоке"
            )
        )
        container.add_item(Separator())

        container.add_item(
            TextDisplay(f"### Общее количество: {len(participants)}")
        )

        text = "Пока нет участников. Будьте первым, кто зарегистрируется!"
        if participants:
            text = "\n".join(
                f"<:pets:1480954494354194473> <@{p.user_id}>: {p.song_artist}, {p.song_title}"  # noqa: E501
                for p in participants
            )

        container.add_item(TextDisplay(text))

        self.add_item(container)
