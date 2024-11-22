from typing import TYPE_CHECKING

from app.config.settings import TaskSettings
from app.infrastructure.saq import TaskContext
from app.modules.story.application.services import StoryService
from app.modules.story.application.use_cases import RefreshStoryUseCase


if TYPE_CHECKING:
    from aioinject import InjectionContext  # noqa: F401


async def refresh_all_stories_job(ctx: TaskContext) -> None:
    queue = ctx['worker'].queue
    async with ctx['container'].context() as container_ctx:  # type: InjectionContext
        service = await container_ctx.resolve(StoryService)
        task_settings = await container_ctx.resolve(TaskSettings)
        for code in await service.get_all_stories():
            await queue.enqueue(
                'refresh_story_task',
                code=code,
                timeout=task_settings.RUNTIME_TIMEOUT_SECONDS,
            )


async def refresh_story_task(ctx: TaskContext, *, id_: int) -> None:
    async with ctx['container'].context() as container_ctx:  # type: InjectionContext
        use_case = await container_ctx.resolve(RefreshStoryUseCase)
        await use_case.execute(id_=id_)
