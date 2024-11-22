import logging

import saq

from app.config import settings
from app.di.container import create_container
from app.infrastructure.logging import configure_logging
from app.infrastructure.saq import SaqQueue, TaskContext, saq_queue
from app.modules.story.application.tasks import (
    refresh_all_stories_job,
    refresh_story_task,
)


logger = logging.getLogger(__name__)


async def startup(ctx: TaskContext) -> None:
    configure_logging()

    logger.info('Worker init')
    if logger.isEnabledFor(logging.DEBUG):
        info = await ctx['worker'].queue.info()
        logger.debug('Worker info: %s', info)

    ctx['container'] = create_container()


async def shutdown(ctx: TaskContext) -> None:
    await ctx['container'].aclose()


async def async_check_health(queue: SaqQueue) -> int:
    info = await queue.info()
    name = info.get('name')
    if name != queue.name:
        logger.warning(
            'Health check failed. Unknown queue name %s. Expected %s',
            name,
            queue.name,
        )
        status = 1
    elif not info.get('workers'):
        logger.warning('No active workers found for queue %s', name)
        status = 1
    else:
        workers = len(info['workers'].values())
        logger.info('Found %d active workers for queue %s', workers, name)
        status = 0

    await queue.disconnect()
    return status


# Monkeypatch
# TODO: When new saq version released
saq.worker.async_check_health = async_check_health  # type: ignore[assignment]

saq_settings = {
    'queue': saq_queue,
    'functions': [
        refresh_story_task,
    ],
    'cron_jobs': [
        saq.CronJob(
            refresh_all_stories_job,
            cron=settings.task.REFRESH_STORY_SCHEDULE,
        ),
    ],
    'startup': startup,
    'shutdown': shutdown,
}
