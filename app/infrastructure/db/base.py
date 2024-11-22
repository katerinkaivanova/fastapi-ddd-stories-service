from datetime import datetime

from sqlalchemy import DateTime, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

from app.seedwork.utils.dt import get_utc_now


# Default naming convention for all indexes and constraints
# See why this is important and how it would save your time:
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(naming_convention=convention)
    registry = registry(  # mapping of Python types to SQLAlchemy TypeEngine types
        type_annotation_map={
            datetime: DateTime(timezone=True),
        },
    )

    created_at: Mapped[datetime] = mapped_column(default=get_utc_now())
    modified_at: Mapped[datetime] = mapped_column(
        default=get_utc_now(),
        onupdate=get_utc_now(),
    )
