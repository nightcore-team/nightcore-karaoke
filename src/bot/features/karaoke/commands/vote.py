"""Vote command."""

import logging
from typing import TYPE_CHECKING, cast

from discord import Guild, Interaction, User, app_commands
from discord.ext.commands import Cog  # type: ignore

from src.bot.components.embed import ErrorEmbed, SuccessEmbed
from src.bot.decorators.permissions import (
    PermissionFlagEnum,
    check_required_permissions,
)
from src.bot.features.karaoke.utils.autocomplete import (
    vote_registration_autocomplete,
)
from src.infra.db.enums import KaraokeStateEnum
from src.infra.db.operations import (
    create_rating,
    get_karaoke_by_guild_id,
    get_rating_for_registration,
    get_registration_by_id,
)

if TYPE_CHECKING:
    from src.bot.client import NightcoreKaraoke
    from src.infra.db.models import Karaoke, Rating, Registration


logger = logging.getLogger(__name__)


class Vote(Cog):
    def __init__(self) -> None:
        super().__init__()

    @app_commands.command(
        name="vote",
        description="Проголосовать за выступление участника (только для судей).",  # noqa: E501
    )  # type: ignore
    @check_required_permissions(PermissionFlagEnum.JUDGE_ACCESS)  # type: ignore
    @app_commands.autocomplete(registration_id=vote_registration_autocomplete)  # type: ignore
    @app_commands.rename(
        user="участник",
        registration_id="песня",
        score="оценка",
    )
    async def vote(
        self,
        interaction: Interaction["NightcoreKaraoke"],
        user: User,
        registration_id: str,
        score: app_commands.Range[int, 1, 10],
    ):
        """Vote command."""
        guild = cast(Guild, interaction.guild)

        match registration_id:
            case "error_no_user":
                return await interaction.response.send_message(
                    embed=ErrorEmbed(
                        error_message="Сначала выберите участника (аргумент 'участник').",  # noqa: E501
                        bot=interaction.client,
                    ),
                    ephemeral=True,
                )

            case "error_no_registrations":
                return await interaction.response.send_message(
                    embed=ErrorEmbed(
                        error_message="Нет доступных песен для голосования. Убедитесь, что участник зарегистрировался с песней.",  # noqa: E501
                        bot=interaction.client,
                    ),
                    ephemeral=True,
                )

            case _ if registration_id.isdigit():
                reg_id = int(registration_id)

            case _:
                return await interaction.response.send_message(
                    embed=ErrorEmbed(
                        error_message="Неверный ID регистрации.",
                        bot=interaction.client,
                    ),
                    ephemeral=True,
                )

        outcome = ""
        karaoke: Karaoke | None = None
        registration: Registration | None = None
        existing_rating: Rating | None = None

        async with interaction.client.uow.start() as session:
            karaoke = await get_karaoke_by_guild_id(session, guild.id)

            if not karaoke:
                outcome = "no_active_karaoke"
            elif karaoke.state != KaraokeStateEnum.GOING:
                outcome = "karaoke_not_going"
            else:
                registration = await get_registration_by_id(session, reg_id)

                if not registration:
                    outcome = "registration_not_found"
                elif registration.karaoke_id != karaoke.id:
                    outcome = "registration_wrong_karaoke"
                else:
                    existing_rating = await get_rating_for_registration(
                        session,
                        karaoke.id,
                        registration.id,
                        interaction.user.id,
                    )

                    if existing_rating:
                        outcome = "already_voted"
                    else:
                        await create_rating(
                            session=session,
                            guild_id=guild.id,
                            karaoke_id=karaoke.id,
                            registration_id=registration.id,
                            user_id=registration.user_id,
                            judge_id=interaction.user.id,
                            score=score,
                        )
                        outcome = "success"

        if outcome == "no_active_karaoke":
            embed = ErrorEmbed(
                error_message="В данный момент нет активного караоке.",
                bot=interaction.client,
            )
        elif outcome == "karaoke_not_going":
            embed = ErrorEmbed(
                error_message="Голосование доступно только когда караоке идёт.",  # noqa: E501
                bot=interaction.client,
            )
        elif outcome == "registration_not_found":
            embed = ErrorEmbed(
                error_message="Регистрация с таким ID не найдена.",
                bot=interaction.client,
            )
        elif outcome == "registration_wrong_karaoke":
            embed = ErrorEmbed(
                error_message="Эта регистрация не относится к текущему караоке.",  # noqa: E501
                bot=interaction.client,
            )
        elif outcome == "already_voted":
            embed = ErrorEmbed(
                error_message="Вы уже проголосовали за это выступление.",
                bot=interaction.client,
            )
        elif outcome == "success":
            embed = SuccessEmbed(
                message=f"Вы успешно проголосовали за участника {user.mention} с оценкой **{score}**!",  # noqa: E501
                bot=interaction.client,
            )
        else:
            embed = ErrorEmbed(
                error_message="Произошла неизвестная ошибка.",
                bot=interaction.client,
            )

        return await interaction.response.send_message(
            embed=embed, ephemeral=True
        )


async def setup(bot: "NightcoreKaraoke") -> None:
    """Setup function for the vote command."""
    await bot.add_cog(Vote())
