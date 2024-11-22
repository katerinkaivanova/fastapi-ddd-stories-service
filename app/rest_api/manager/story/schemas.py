from typing import Literal, Self

from pydantic import AwareDatetime

from app.modules.story.application.dto import StoryOutDTO
from app.rest_api.manager.page.schemas import PageListRelatedObject, PageRelatedObject
from app.rest_api.utils import KebabCaseModel, SchemaModel


class StoryAttributes(KebabCaseModel):
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


class StoryRelationships(KebabCaseModel):
    pages: PageListRelatedObject | None


class StoryCreateObject(SchemaModel):
    type: Literal['stories'] = 'stories'
    attributes: StoryAttributes


class StoryUpdateObject(SchemaModel):
    id: str | None = None
    type: Literal['stories'] = 'stories'
    attributes: StoryAttributes
    relationships: StoryRelationships


class StoryObject(SchemaModel):
    id: str | None = None
    type: Literal['stories'] = 'stories'
    attributes: StoryAttributes
    relationships: StoryRelationships

    @classmethod
    def from_dto(cls, dto: StoryOutDTO) -> Self:
        return cls(
            id=str(dto.id),
            type='stories',
            attributes=StoryAttributes(
                name=dto.name,
                story_type=dto.story_type,
                delay=dto.delay,
                is_disabled=dto.is_disabled,
                is_blocking=dto.is_blocking,
                is_preview=dto.is_preview,
                is_repetitive=dto.is_repetitive,
                is_autoscroll=dto.is_autoscroll,
                publication_start_time=dto.publication_start_time,
                publication_end_time=dto.publication_end_time,
            ),
            relationships=StoryRelationships(
                pages=PageListRelatedObject(
                    data=[PageRelatedObject.from_dto(dto) for dto in dto.pages]
                    if dto.pages
                    else [],
                ),
            ),
        )


class StoryCreateJsonApi(SchemaModel):
    data: StoryCreateObject


class StoryUpdateJsonApi(SchemaModel):
    data: StoryUpdateObject


class StoryJsonApi(SchemaModel):
    data: StoryObject


class LimitOffsetPaginationMeta(SchemaModel):
    limit: int
    offset: int


class StoryListJsonApi(KebabCaseModel):
    meta: LimitOffsetPaginationMeta
    data: list[StoryObject]
