import logging
from typing import final

from app.config.settings import TaskSettings
from app.infrastructure.saq import SaqQueue
from app.modules.story.application.dto import StoryOutDTO
from app.modules.story.application.services import StoryService


logger = logging.getLogger(__name__)


@final
class RefreshStoryUseCase:
    def __init__(
        self,
        story_service: StoryService,
        saq_queue: SaqQueue,
        task_settings: TaskSettings,
    ) -> None:
        self._story_service = story_service
        self._saq_queue = saq_queue
        self._task_settings = task_settings

    async def execute(self, id_: int) -> None:
        story: StoryOutDTO | None = await self._story_service.get_story(id_)

        if story is None:
            return

    async def _run_task(self, id_: int) -> None:
        await self._saq_queue.enqueue(
            'upload_story_task',
            code=id_,
            timeout=self._task_settings.RUNTIME_TIMEOUT_SECONDS,
        )
