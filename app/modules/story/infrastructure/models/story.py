import datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Boolean, String, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db import Base


if TYPE_CHECKING:
    from .page import PageModel


StoryType = Literal['install', 'update', 'info']


class StoryModel(Base):
    __tablename__ = 'story'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), server_default='')
    story_type: Mapped[StoryType] = mapped_column(server_default='info')
    delay: Mapped[int] = mapped_column(nullable=True)
    is_disabled: Mapped[bool] = mapped_column(Boolean, server_default=sql.true())
    is_blocking: Mapped[bool] = mapped_column(Boolean, server_default=sql.false())
    is_preview: Mapped[bool] = mapped_column(Boolean, server_default=sql.false())
    is_repetitive: Mapped[bool] = mapped_column(Boolean, server_default=sql.false())
    is_autoscroll: Mapped[bool] = mapped_column(Boolean, server_default=sql.false())
    publication_start_time: Mapped[datetime.datetime] = mapped_column(nullable=True)
    publication_end_time: Mapped[datetime.datetime] = mapped_column(nullable=True)

    pages: Mapped[list['PageModel']] = relationship(
        lazy='selectin',
        back_populates='story',
        cascade='all, delete-orphan',
    )
