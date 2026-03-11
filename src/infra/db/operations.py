"""Database operations module."""

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infra.db.enums import KaraokeRoleEnum, KaraokeStateEnum

from .models import (
    GuildKaraokeConfig,
    GuildPermissionsConfig,
    Karaoke,
    Rating,
    Registration,
    Staff,
)


async def get_karaoke_config(
    session: AsyncSession, guild_id: int
) -> GuildKaraokeConfig | None:
    """Fetch the karaoke configuration for a specific guild."""

    result = await session.execute(
        select(GuildKaraokeConfig).where(
            GuildKaraokeConfig.guild_id == guild_id
        )
    )
    return result.scalar_one_or_none()


async def get_permissions_config(
    session: AsyncSession, guild_id: int
) -> GuildPermissionsConfig | None:
    """Fetch the permissions configuration for a specific guild."""

    result = await session.execute(
        select(GuildPermissionsConfig).where(
            GuildPermissionsConfig.guild_id == guild_id
        )
    )
    return result.scalar_one_or_none()


async def get_karaoke_config_access_roles(
    session: AsyncSession, guild_id: int
) -> list[int] | None:
    """Fetch the karaoke config access roles for a specific guild."""

    result = await session.execute(
        select(GuildPermissionsConfig.karaoke_config_access_roles_ids).where(
            GuildPermissionsConfig.guild_id == guild_id
        )
    )
    return result.scalar_one_or_none()


async def get_user_staff_role(
    session: AsyncSession, guild_id: int, user_id: int
) -> KaraokeRoleEnum | None:
    """Fetch the staff role of a user in a specific guild."""

    result = await session.execute(
        select(Staff).where(
            Staff.guild_id == guild_id, Staff.user_id == user_id
        )
    )

    result = result.scalar_one_or_none()
    return result.role if result else None


async def create_staff(
    session: AsyncSession, guild_id: int, user_id: int, role: KaraokeRoleEnum
) -> Staff:
    """Create a staff member in the database."""

    staff = Staff(guild_id=guild_id, user_id=user_id, role=role)
    session.add(staff)

    return staff


async def update_staff_role(
    session: AsyncSession, guild_id: int, user_id: int, role: KaraokeRoleEnum
) -> Staff | None:
    """Update staff role for an existing guild user binding."""

    result = await session.execute(
        select(Staff).where(
            Staff.guild_id == guild_id, Staff.user_id == user_id
        )
    )

    staff = result.scalar_one_or_none()
    if staff is None:
        return None

    staff.role = role
    return staff


async def delete_staff(
    session: AsyncSession, guild_id: int, user_id: int
) -> bool:
    """Delete staff binding for a guild user."""

    result = await session.execute(
        select(Staff).where(
            Staff.guild_id == guild_id, Staff.user_id == user_id
        )
    )

    staff = result.scalar_one_or_none()
    if staff is None:
        return False

    await session.delete(staff)
    return True


async def get_karaokes_by_guild_id(
    session: AsyncSession, guild_id: int
) -> list[Karaoke]:
    """Get all karaokes for a specific guild."""

    result = await session.execute(
        select(Karaoke).where(Karaoke.guild_id == guild_id)
    )
    return result.scalars().all()  # type: ignore


async def get_karaoke_by_guild_id(
    session: AsyncSession, guild_id: int, with_registrations: bool = False
) -> Karaoke | None:
    """Get a karaoke for a specific guild."""

    stmt = (
        select(Karaoke)
        .where(
            Karaoke.guild_id == guild_id,
            Karaoke.state != KaraokeStateEnum.FINISHED,
        )
        .order_by(Karaoke.updated_at.desc())
        .limit(1)
    )
    if with_registrations:
        stmt = stmt.options(selectinload(Karaoke.registrations))

    result = await session.execute(stmt)

    return result.scalar_one_or_none()


async def get_karaoke_by_id(
    session: AsyncSession, karaoke_id: int, with_registrations: bool = False
) -> Karaoke | None:
    """Get a karaoke by its ID."""

    stmt = select(Karaoke).where(Karaoke.id == karaoke_id)

    if with_registrations:
        stmt = stmt.options(selectinload(Karaoke.registrations))

    result = await session.execute(stmt)

    return result.scalar_one_or_none()


async def create_karaoke(
    session: AsyncSession,
    guild_id: int,
    host_id: int,
    name: str,
    description: str | None,
    prizes: list[str] | None,
) -> Karaoke:
    """Create a karaoke for a specific guild."""

    karaoke = Karaoke(
        guild_id=guild_id,
        host_id=host_id,
        name=name,
        description=description,
        prizes=prizes,
    )
    session.add(karaoke)

    return karaoke


async def create_karaoke_registration(
    session: AsyncSession,
    guild_id: int,
    karaoke_id: int,
    user_id: int,
    song_artist: str,
    song_title: str,
) -> Registration:
    """Create a karaoke registration for a specific karaoke."""

    registration = Registration(
        guild_id=guild_id,
        karaoke_id=karaoke_id,
        user_id=user_id,
        song_artist=song_artist,
        song_title=song_title,
    )
    session.add(registration)

    return registration


async def get_karaoke_results(
    session: AsyncSession, karaoke_id: int
) -> list[tuple[Registration, float]]:
    """Get the calculated average score for each registration in a karaoke session.

    Returns:
        A list of tuples with the registration and the average score.
    """  # noqa: E501
    stmt = (
        select(Registration, func.avg(Rating.score).label("average_score"))
        .join(Rating, Rating.registration_id == Registration.id)
        .where(Registration.karaoke_id == karaoke_id)
        .group_by(Registration.id)
        .order_by(desc("average_score"))
    )
    result = await session.execute(stmt)

    return result.all()  # type: ignore


async def get_registration_by_id(
    session: AsyncSession, registration_id: int
) -> Registration | None:
    """Get a registration by its ID."""

    result = await session.execute(
        select(Registration).where(Registration.id == registration_id)
    )
    return result.scalar_one_or_none()


async def get_rating_for_registration(
    session: AsyncSession,
    karaoke_id: int,
    registration_id: int,
    judge_id: int,
) -> Rating | None:
    """Get a rating for a specific registration from a specific judge."""

    result = await session.execute(
        select(Rating).where(
            Rating.karaoke_id == karaoke_id,
            Rating.registration_id == registration_id,
            Rating.judge_id == judge_id,
        )
    )
    return result.scalar_one_or_none()


async def create_rating(
    session: AsyncSession,
    guild_id: int,
    karaoke_id: int,
    registration_id: int,
    user_id: int,
    judge_id: int,
    score: int,
) -> Rating:
    """Create a rating for a karaoke registration."""

    rating = Rating(
        guild_id=guild_id,
        karaoke_id=karaoke_id,
        registration_id=registration_id,
        user_id=user_id,
        judge_id=judge_id,
        score=score,
    )
    session.add(rating)

    return rating
