from typing import Literal, Self

from pydantic import AwareDatetime

from app.modules.story.application.dto import PageOutDTO
from app.rest_api.utils import KebabCaseModel, SchemaModel


class PageImage(SchemaModel):
    url: str
    platform: str


class PageAttributes(KebabCaseModel):
    created_at: AwareDatetime | None = None
    modified_at: AwareDatetime | None = None


class PageObject(SchemaModel):
    id: str | None = None
    type: Literal['pages'] = 'pages'
    attributes: PageAttributes

    @classmethod
    def from_dto(cls, dto: PageOutDTO) -> Self:
        return cls(
            id=str(dto.id),
            type='pages',
            attributes=PageAttributes(
                created_at=dto.created_at,
                modified_at=dto.modified_at,
            ),
        )


class PageJsonApi(SchemaModel):
    data: PageObject


class LimitOffsetPaginationMeta(SchemaModel):
    limit: int
    offset: int


class PageListJsonApi(KebabCaseModel):
    meta: LimitOffsetPaginationMeta
    data: list[PageObject]


class PageRelatedObject(SchemaModel):
    id: str | None = None
    type: Literal['pages'] = 'pages'

    @classmethod
    def from_dto(cls, dto: PageOutDTO) -> Self:
        return cls(
            id=str(dto.id),
            type='pages',
        )


class PageListRelatedObject(SchemaModel):
    data: list[PageRelatedObject]
