from collections.abc import Iterable
from typing import Any

from aioinject import Provider
from aioinject.providers import Scoped

from app.modules.story.application.services import StoryService
from app.modules.story.domain.repositories import IStoryRepository
from app.modules.story.infrastructure.repositories import SqlAlchemyStoryRepository


__all__ = ['providers']

providers: Iterable[Provider[Any]] = (
    Scoped(StoryService),
    Scoped(SqlAlchemyStoryRepository, IStoryRepository),
)
