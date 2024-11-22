from typing import TYPE_CHECKING, TypeAlias

from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff

from app.config.settings import RedisSettings


if TYPE_CHECKING:
    RedisClient: TypeAlias = Redis[str]  # type: ignore
else:
    RedisClient = Redis


def get_redis_client(settings: RedisSettings) -> RedisClient:
    return RedisClient.from_url(
        url=str(settings.HOST),
        decode_responses=True,
        retry=Retry(ExponentialBackoff(), 3),  # type: ignore
        retry_on_timeout=True,
    )
