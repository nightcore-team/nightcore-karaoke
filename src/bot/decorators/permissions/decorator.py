"""Decorator to check for required permissions before executing a command."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    ParamSpec,
    TypeVar,
    cast,
    overload,
)

from discord import Guild, Interaction, Member, app_commands

from src.config._global import config as global_config
from src.infra.db.operations import (
    KaraokeRoleEnum,
    get_permissions_config,
    get_user_staff_role,
)

if TYPE_CHECKING:
    from discord.ext.commands import Cog  # type: ignore

    from src.bot.client import NightcoreKaraoke

from .types import PermissionFlagEnum

P = ParamSpec("P")
T = TypeVar("T")
CogT = TypeVar("CogT", bound="Cog")


@overload
def check_required_permissions(  # type: ignore
    permissions_flag: PermissionFlagEnum,
) -> Callable[
    [Callable[Concatenate[Interaction[NightcoreKaraoke], P], Awaitable[T]]],
    Callable[Concatenate[Interaction[NightcoreKaraoke], P], Awaitable[T]],
]: ...


@overload
def check_required_permissions(  # type: ignore
    permissions_flag: PermissionFlagEnum,
) -> Callable[
    [
        Callable[
            Concatenate[CogT, Interaction[NightcoreKaraoke], P], Awaitable[T]
        ]
    ],
    Callable[
        Concatenate[CogT, Interaction[NightcoreKaraoke], P], Awaitable[T]
    ],
]: ...


def check_required_permissions(
    permissions_flag: PermissionFlagEnum,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator to check for required permissions before executing a command.

    Args:
        permissions_flag: Required permission flag

    Returns:
        Decorated function with permission check

    Example:
        # In Cog:
        ```
        @check_required_permissions(PermissionsFlagEnum.ADMINISTRATOR)
        async def my_command(self, interaction: Interaction):
            ...
        ```

        # Standalone:
        ```
        @check_required_permissions(PermissionsFlagEnum.ADMINISTRATOR)
        async def my_function(interaction: Interaction):
            ...
        ```
    """

    def decorator(
        func: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            interaction: Interaction[NightcoreKaraoke] | None = None

            for arg in args:
                if isinstance(arg, Interaction):
                    interaction = arg  # type: ignore
                    break

            if not interaction and "interaction" in kwargs:
                interaction = kwargs["interaction"]

            if not interaction:
                raise ValueError(
                    f"Interaction not found in {func.__class__.__qualname__} arguments"  # noqa: E501
                )

            has_permission = await _check_user_permission(
                interaction, permissions_flag
            )

            if not has_permission:
                raise app_commands.MissingPermissions(
                    missing_permissions=[permissions_flag.value]
                )

            func.__permissions_flag__ = permissions_flag  # type: ignore

            return await func(*args, **kwargs)

        wrapper.__permissions_flag__ = permissions_flag  # type: ignore

        return wrapper

    return decorator


async def _check_user_permission(
    interaction: Interaction[NightcoreKaraoke],
    permissions: PermissionFlagEnum,
) -> bool:
    """Check if user has required permission.

    Args:
        interaction: Discord interaction
        permissions: Required permission flag

    Returns:
        True if user has permission, False otherwise
    """

    guild = cast(Guild, interaction.guild)

    if not hasattr(cast(Member, interaction.user), "guild_permissions"):
        return False

    if permissions == PermissionFlagEnum.UNSAFE:
        """
            >>> UNSAFE permission bypasses all checks and always returns True.
            So, if a command is marked with UNSAFE, it means that you have
            to check manually user's permissions inside the command implementation.
        """  # noqa: E501

        return True

    if permissions == PermissionFlagEnum.NONE:
        return True

    if permissions == PermissionFlagEnum.BOT_ACCESS:
        return interaction.user.id in global_config.bot.DEVELOPERS_IDS

    if permissions == PermissionFlagEnum.KARAOKE_CONFIG_ACCESS:
        async with interaction.client.uow.start(readonly=True) as session:
            permissions_config = await get_permissions_config(
                session, guild.id
            )

        if permissions_config is None:
            return False

        access_roles_ids = set(
            permissions_config.karaoke_config_access_roles_ids or []
        )

        return any(
            role.id in access_roles_ids
            for role in cast(Member, interaction.user).roles
        )

    if permissions == PermissionFlagEnum.HOST_ACCESS:
        async with interaction.client.uow.start(readonly=True) as session:
            user_role = await get_user_staff_role(
                session, guild.id, interaction.user.id
            )

        return user_role == KaraokeRoleEnum.HOST

    if permissions == PermissionFlagEnum.JUDGE_ACCESS:
        async with interaction.client.uow.start(readonly=True) as session:
            user_role = await get_user_staff_role(
                session, guild.id, interaction.user.id
            )

        return user_role in (KaraokeRoleEnum.JUDGE, KaraokeRoleEnum.HOST)

    return False
