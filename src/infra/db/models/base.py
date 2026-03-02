"""Base model for SQLAlchemy ORM with async support."""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.infra.db.mixins import IdIntegerMixin, TimestampMixin


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(self) -> str:
        """Generate table name from class name."""
        return f"{self.__name__.lower()}"


class BaseIdTimeStampModel(Base, IdIntegerMixin, TimestampMixin):
    """Base model with id and timestamp fields."""

    __abstract__ = True
