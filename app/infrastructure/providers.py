from collections.abc import Iterable
from typing import Any

from aioinject.providers import Object, Provider, Scoped, Singleton

from app.config import settings
from app.config.settings import (
    RedisSettings,
    StorySettings,
    TaskSettings,
)
from app.infrastructure.db import db_manager
from app.infrastructure.redis import RedisClient, get_redis_client
from app.infrastructure.saq import SaqQueue, saq_queue


__all__ = ['providers']


providers: Iterable[Provider[Any]] = (
    # Postgres
    Scoped(db_manager.session),
    # Redis
    Object(settings.redis, RedisSettings),
    Singleton(get_redis_client, RedisClient),
    # Saq
    Object(saq_queue, SaqQueue),
    # Story
    Object(settings.story, StorySettings),
    # Task
    Object(settings.task, TaskSettings),
)
