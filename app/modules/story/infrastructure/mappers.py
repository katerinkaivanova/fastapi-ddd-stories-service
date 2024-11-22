from app.modules.story.domain.entities import PageEntity, PageId, StoryEntity, StoryId
from app.modules.story.infrastructure.models import PageModel, StoryModel


__all__ = [
    'map_entity_to_story_model',
    'map_story_model_to_entity',
]


def map_entity_to_page_model(entity: PageEntity) -> PageModel:
    return PageModel(
        id=entity.id or None,
        created_at=entity.created_at,
        modified_at=entity.modified_at,
        story_id=entity.story_id,
    )


def map_page_model_to_entity(model: PageModel) -> PageEntity:
    return PageEntity(
        id=PageId(model.id),
        created_at=model.created_at,
        modified_at=model.modified_at,
        story_id=StoryId(model.story_id),
    )


def map_entity_to_story_model(entity: StoryEntity) -> StoryModel:
    return StoryModel(
        id=entity.id or None,
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
        pages=entity.pages,
    )


def map_story_model_to_entity(model: StoryModel) -> StoryEntity:
    return StoryEntity(
        id=StoryId(model.id),
        name=model.name,
        story_type=model.story_type,
        delay=model.delay,
        is_disabled=model.is_disabled,
        is_blocking=model.is_blocking,
        is_preview=model.is_preview,
        is_repetitive=model.is_repetitive,
        is_autoscroll=model.is_autoscroll,
        publication_start_time=model.publication_start_time,
        publication_end_time=model.publication_end_time,
        created_at=model.created_at,
        modified_at=model.modified_at,
        pages=[map_page_model_to_entity(page) for page in model.pages],
    )
