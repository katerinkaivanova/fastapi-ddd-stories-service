from dataclasses import dataclass
from typing import Self

from app.modules.story.domain.entities import PageEntity, StoryEntity


__all__ = [
    'StoryCreateDTO',
    'StoryOutDTO',
    'StoryUpdateDTO',
]


from pydantic import AwareDatetime


@dataclass(kw_only=True)
class PageOutDTO:
    id: int
    created_at: AwareDatetime | None
    modified_at: AwareDatetime | None

    @classmethod
    def from_entity(cls, entity: PageEntity) -> Self:
        return cls(
            id=entity.id,
            created_at=entity.created_at,
            modified_at=entity.modified_at,
        )


@dataclass(kw_only=True)
class StoryCreateDTO:
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


@dataclass(kw_only=True)
class StoryUpdateDTO:
    id: int
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

    pages: list[PageOutDTO] | None


@dataclass(kw_only=True)
class StoryOutDTO:
    id: int
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

    pages: list[PageOutDTO] | None

    @classmethod
    def from_entity(cls, entity: StoryEntity) -> Self:
        return cls(
            id=entity.id,
            name=entity.name,
            story_type=entity.story_type,
            delay=entity.delay,
            is_disabled=entity.is_disabled,
            is_blocking=entity.is_blocking,
            is_preview=entity.is_preview,
            is_repetitive=entity.is_repetitive,
            is_autoscroll=entity.is_autoscroll,
            publication_start_time=entity.publication_start_time,
            publication_end_time=entity.publication_end_time,
            pages=[PageOutDTO.from_entity(page) for page in entity.pages]
            if entity.pages
            else [],
        )
