import abc

from app.modules.story.domain.entities import StoryEntity
from app.seedwork.domain.repositories import IBaseRepository


__all__ = ['IStoryRepository']


class IStoryRepository(IBaseRepository[StoryEntity], metaclass=abc.ABCMeta):
    entity_cls = StoryEntity

    @abc.abstractmethod
    async def get_all(self) -> list[StoryEntity]:
        ...
