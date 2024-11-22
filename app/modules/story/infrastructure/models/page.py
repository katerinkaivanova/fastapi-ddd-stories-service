from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db import Base


if TYPE_CHECKING:
    from .story import StoryModel


class PageModel(Base):
    __tablename__ = 'page'

    id: Mapped[int] = mapped_column(primary_key=True)
    story_id: Mapped[int] = mapped_column(ForeignKey('story.id'))

    story: Mapped['StoryModel'] = relationship(
        lazy='joined',
        back_populates='pages',
    )
