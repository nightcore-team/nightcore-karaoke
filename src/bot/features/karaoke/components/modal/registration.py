"""Karaoke registration modal component."""

from discord import TextStyle
from discord.ui import Modal, TextInput


class KaraokeRegistrationModal(Modal):
    song_artist = TextInput["KaraokeRegistrationModal"](
        label="Введите имя исполнителя",
        style=TextStyle.short,
        placeholder="Пример: Nightcore",
        required=True,
        max_length=255,
    )

    song_title = TextInput["KaraokeRegistrationModal"](
        label="Введите название песни",
        style=TextStyle.short,
        placeholder="Пример: Blinding Lights",
        required=True,
        max_length=255,
    )

    def __init__(self, karaoke_id: int) -> None:
        super().__init__(
            title="Зарегистрировать песню",
            timeout=None,
            custom_id=f"karaoke:register_modal:{karaoke_id}",
        )
        self.karaoke_id = karaoke_id
