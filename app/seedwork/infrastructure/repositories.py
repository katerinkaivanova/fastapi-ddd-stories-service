import abc
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import Base
from app.seedwork.domain.entities import EntityId, EntityT
from app.seedwork.domain.exceptions import EntityNotFoundException
from app.seedwork.domain.repositories import IBaseRepository


__all__ = [
    'ModelT',
    'SqlAlchemyBaseRepository',
]


ModelT = TypeVar('ModelT', bound=Base)


class SqlAlchemyBaseRepository(
    IBaseRepository[EntityT],
    Generic[EntityT, ModelT],
    metaclass=abc.ABCMeta,
):
    entity_cls: type[EntityT]
    model_cls: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, entity: EntityT) -> EntityT:
        mapped_model = self._map_entity_to_model(entity)
        self._session.add(mapped_model)
        await self._session.flush()
        return self._map_model_to_entity(mapped_model)

    async def update(self, entity: EntityT) -> EntityT:
        mapped_model = self._map_entity_to_model(entity)
        merged = await self._session.merge(mapped_model)
        self._session.add(merged)
        return self._map_model_to_entity(merged)

    async def remove(self, entity: EntityT) -> None:
        model = await self._session.get(self.model_cls, entity.id)
        await self._session.delete(model)

    async def remove_by_id(self, entity_id: EntityId) -> None:
        model = await self._session.get(self.model_cls, entity_id)
        if not model:
            raise EntityNotFoundException(
                entity_type=self.entity_cls,
                kwargs={'id': entity_id},
            )
        await self._session.delete(model)

    async def get_by_id(self, entity_id: EntityId) -> EntityT:
        model = await self._session.get(self.model_cls, entity_id)
        if not model:
            raise EntityNotFoundException(
                entity_type=self.entity_cls,
                kwargs={'id': entity_id},
            )
        return self._map_model_to_entity(model)

    @classmethod
    @abc.abstractmethod
    def _map_entity_to_model(cls, entity: EntityT) -> ModelT:
        ...

    @classmethod
    @abc.abstractmethod
    def _map_model_to_entity(cls, model: ModelT) -> EntityT:
        ...
