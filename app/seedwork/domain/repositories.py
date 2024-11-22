import abc
from typing import Generic

from app.seedwork.domain.entities import EntityId, EntityT


__all__ = ['IBaseRepository']


class IBaseRepository(Generic[EntityT], metaclass=abc.ABCMeta):
    entity_cls: type[EntityT]

    @abc.abstractmethod
    async def add(self, entity: EntityT) -> EntityT:
        ...

    @abc.abstractmethod
    async def update(self, entity: EntityT) -> EntityT:
        ...

    @abc.abstractmethod
    async def remove(self, entity: EntityT) -> None:
        ...

    @abc.abstractmethod
    async def remove_by_id(self, entity_id: EntityId) -> None:
        ...

    @abc.abstractmethod
    async def get_by_id(self, entity_id: EntityId) -> EntityT:
        ...
