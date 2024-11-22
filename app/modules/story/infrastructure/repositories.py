from sqlalchemy import select

from app.modules.story.domain.entities import StoryEntity
from app.modules.story.domain.repositories import IStoryRepository
from app.modules.story.infrastructure.mappers import (
    map_entity_to_story_model,
    map_story_model_to_entity,
)
from app.modules.story.infrastructure.models import StoryModel
from app.seedwork.infrastructure.repositories import SqlAlchemyBaseRepository


__all__ = ['SqlAlchemyStoryRepository']


class SqlAlchemyStoryRepository(
    IStoryRepository,
    SqlAlchemyBaseRepository[StoryEntity, StoryModel],
):
    entity_cls = StoryEntity
    model_cls = StoryModel

    async def get_all(self) -> list[StoryEntity]:
        objs = await self._session.scalars(select(self.model_cls))
        return [self._map_model_to_entity(obj) for obj in objs]

    @classmethod
    def _map_entity_to_model(cls, entity: StoryEntity) -> StoryModel:
        return map_entity_to_story_model(entity)

    @classmethod
    def _map_model_to_entity(cls, model: StoryModel) -> StoryEntity:
        return map_story_model_to_entity(model)
