from dataclasses import dataclass
from typing import NewType

from pydantic import AwareDatetime

from app.seedwork.domain.entities import Entity


__all__ = [
    'PageEntity',
    'PageId',
    'StoryEntity',
    'StoryId',
]


PageId = NewType('PageId', int)
StoryId = NewType('StoryId', int)


@dataclass(kw_only=True)
class PageEntity(Entity[PageId]):
    created_at: AwareDatetime | None
    modified_at: AwareDatetime | None

    story_id: int


@dataclass(kw_only=True)
class StoryEntity(Entity[StoryId]):
    name: str
    story_type: str
    delay: int | None
    is_disabled: bool
    is_blocking: bool
    is_preview: bool
    is_repetitive: bool
    is_autoscroll: bool

    publication_start_time: AwareDatetime | None
    publication_end_time: AwareDatetime | None

    created_at: AwareDatetime | None
    modified_at: AwareDatetime | None

    pages: list[PageEntity] | None
