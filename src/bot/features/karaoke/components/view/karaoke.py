"""Karaoke V2 view component."""

from discord import ButtonStyle, Color
from discord.ui import (
    ActionRow,
    Button,
    Container,
    LayoutView,
    Separator,
    TextDisplay,
)


class KaraokeView(LayoutView):
    def __init__(
        self,
        name: str,
        karaoke_id: int,
        description: str | None,
        karaoke_state: str,
        registration_state: str,
        host_id: int,
        prizes: list[str] | None,
    ) -> None:
        super().__init__()

        self.karaoke_id = karaoke_id
        self.name = name
        self.description = description
        self.karaoke_state = karaoke_state
        self.registration_state = registration_state
        self.prizes = prizes
        self.host_id = host_id

    def build(self, disable_buttons: bool = False) -> "KaraokeView":
        """Build the karaoke view layout."""

        container = Container["KaraokeView"](
            accent_color=Color.from_str("#fdcdc9")
        )

        container.add_item(
            TextDisplay(
                f"## <:microphone:1480906998689300491> Караоке: {self.name}"
            )
        )
        if self.description:
            container.add_item(TextDisplay(f"> ### {self.description}"))
        container.add_item(Separator())

        text_components: list[TextDisplay["KaraokeView"]] = [  # noqa: UP037
            TextDisplay(
                f"**Статус: {self.karaoke_state}**\n"
                f"**Статус регистрации: {self.registration_state}**\n"
            ),
            TextDisplay(
                f"## <:cat:1480907224523210752> Организатор: <@{self.host_id}>"
            ),
        ]
        for component in text_components:
            container.add_item(component)
        container.add_item(Separator())

        if self.prizes:
            prizes_text = "\n".join(
                f"> <:pets:1480954494354194473> **{i} место: {prize}**"
                for i, prize in enumerate(self.prizes, 1)
            )
            container.add_item(
                TextDisplay(
                    f"## <:trophy:1480912067887108106> Призы:\n{prizes_text}"
                )
            )

        buttons = ActionRow["KaraokeView"](
            Button(
                label="Список участников",
                custom_id=f"karaoke:participants:{self.karaoke_id}",
                style=ButtonStyle.secondary,
                emoji="<:group:1480910755493712062>",
            ),
        )
        if self.registration_state.lower() == "открыта":
            buttons.add_item(
                Button(
                    label="Зарегистрироваться",
                    custom_id=f"karaoke:register:{self.karaoke_id}",
                    style=ButtonStyle.secondary,
                    emoji="<:pets:1480954494354194473>",
                ),
            )

        if self.karaoke_state.lower() == "завершено":
            buttons.add_item(
                Button(
                    label="Результаты участников",
                    custom_id=f"karaoke:results:{self.karaoke_id}",
                    style=ButtonStyle.secondary,
                    emoji="<:best:1481264243520311296>",
                ),
            )

        container.add_item(Separator())
        container.add_item(buttons)

        self.add_item(container)

        return self
