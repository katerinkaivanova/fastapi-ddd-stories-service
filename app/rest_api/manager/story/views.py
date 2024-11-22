from dataclasses import dataclass
from typing import Annotated, Literal

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Body, Depends, Query
from starlette import status

from app.modules.story.application.dto import StoryCreateDTO, StoryUpdateDTO
from app.modules.story.application.services import StoryService
from app.rest_api.errors import RequestParamValidationError, ResourceNotFoundByIdError
from app.rest_api.manager.story.schemas import (
    LimitOffsetPaginationMeta,
    StoryCreateJsonApi,
    StoryJsonApi,
    StoryListJsonApi,
    StoryObject,
    StoryUpdateJsonApi,
)
from app.rest_api.responses import JSON_API_MEDIA_TYPE, build_responses


StoryServiceDep = Annotated[StoryService, Inject]


router = APIRouter(
    prefix='/stories',
    tags=['stories'],
)


@dataclass(slots=True, kw_only=True)
class ListStoryQueryParams:
    ordering: Annotated[Literal['id', '-id'], Query(max_length=3)] = 'id'
    search: Annotated[str | None, Query(max_length=50)] = None

    story_type: Annotated[
        str | None,
        Query(max_length=50, alias='filter[story-type]'),
    ] = None
    platform_id: Annotated[
        str | None,
        Query(max_length=50, alias='filter[platform-id]'),
    ] = None
    app_version: Annotated[
        str | None,
        Query(max_length=50, alias='filter[app-version]'),
    ] = None
    segment: Annotated[int | None, Query(alias='filter[segment]')] = None
    is_published: Annotated[bool | None, Query(alias='filter[is-published]')] = None
    is_disabled: Annotated[bool | None, Query(alias='filter[is-disabled]')] = None

    limit: Annotated[int, Query(ge=1, le=100)] = 20
    offset: Annotated[int, Query(ge=0)] = 0


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    responses=build_responses(
        status_code=status.HTTP_200_OK,
        response_model=StoryListJsonApi,
        content_type=JSON_API_MEDIA_TYPE,
    ),
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
@inject
async def list_stories(
    p: Annotated[ListStoryQueryParams, Depends()],
    service: StoryServiceDep,
) -> StoryListJsonApi:
    stories = await service.get_all_stories()

    return StoryListJsonApi(
        meta=LimitOffsetPaginationMeta(
            limit=p.limit,
            offset=p.offset,
        ),
        data=[StoryObject.from_dto(dto) for dto in stories],
    )


@router.get(
    '/{story_id}/',
    status_code=status.HTTP_200_OK,
    responses=build_responses(
        status_code=status.HTTP_200_OK,
        response_model=StoryJsonApi,
        content_type=JSON_API_MEDIA_TYPE,
        exceptions=(
            RequestParamValidationError,
            ResourceNotFoundByIdError,
        ),
    ),
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
@inject
async def get_story(
    story_id: int,
    service: StoryServiceDep,
) -> StoryJsonApi:
    story = await service.get_story(story_id)

    return StoryJsonApi(data=StoryObject.from_dto(story))


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses=build_responses(
        status_code=status.HTTP_201_CREATED,
        response_model=StoryJsonApi,
        content_type=JSON_API_MEDIA_TYPE,
        exceptions=(RequestParamValidationError,),
    ),
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
@inject
async def create_story(
    service: StoryServiceDep,
    data: Annotated[StoryCreateJsonApi, Body(media_type=JSON_API_MEDIA_TYPE)],
) -> StoryJsonApi:
    attrs = data.data.attributes
    story = await service.create_story(
        StoryCreateDTO(
            name=attrs.name,
            story_type=attrs.story_type,
            delay=attrs.delay,
            is_disabled=attrs.is_disabled,
            is_blocking=attrs.is_blocking,
            is_preview=attrs.is_preview,
            is_repetitive=attrs.is_repetitive,
            is_autoscroll=attrs.is_autoscroll,
            publication_start_time=attrs.publication_start_time,
            publication_end_time=attrs.publication_end_time,
        ),
    )
    return StoryJsonApi(data=StoryObject.from_dto(story))


@router.put(
    '/{story_id}/',
    status_code=status.HTTP_200_OK,
    responses=build_responses(
        status_code=status.HTTP_200_OK,
        response_model=StoryJsonApi,
        content_type=JSON_API_MEDIA_TYPE,
        exceptions=(
            RequestParamValidationError,
            ResourceNotFoundByIdError,
        ),
    ),
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
@inject
async def update_story(
    story_id: int,
    service: StoryServiceDep,
    data: Annotated[StoryUpdateJsonApi, Body(media_type=JSON_API_MEDIA_TYPE)],
) -> StoryJsonApi:
    attrs = data.data.attributes
    story = await service.update_story(
        StoryUpdateDTO(
            id=story_id,
            name=attrs.name,
            story_type=attrs.story_type,
            delay=attrs.delay,
            is_disabled=attrs.is_disabled,
            is_blocking=attrs.is_blocking,
            is_preview=attrs.is_preview,
            is_repetitive=attrs.is_repetitive,
            is_autoscroll=attrs.is_autoscroll,
            publication_start_time=attrs.publication_start_time,
            publication_end_time=attrs.publication_end_time,
            pages=[],
        ),
    )
    return StoryJsonApi(data=StoryObject.from_dto(story))


@router.delete(
    '/{story_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    responses=build_responses(
        status_code=status.HTTP_204_NO_CONTENT,
        response_model=None,
        content_type=JSON_API_MEDIA_TYPE,
        exceptions=(
            RequestParamValidationError,
            ResourceNotFoundByIdError,
        ),
    ),
)
@inject
async def delete_story(
    story_id: int,
    service: StoryServiceDep,
) -> None:
    await service.delete_story(story_id)
