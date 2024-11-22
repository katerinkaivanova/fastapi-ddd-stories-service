from app.config.settings import TaskSettings
from app.infrastructure.saq import SaqQueue
from app.modules.story.application.dto import StoryCreateDTO, StoryOutDTO, StoryUpdateDTO
from app.modules.story.domain.entities import StoryEntity
from app.modules.story.domain.repositories import IStoryRepository


class StoryService:
    def __init__(
        self,
        repository: IStoryRepository,
        saq_queue: SaqQueue,
        task_settings: TaskSettings,
    ) -> None:
        self._repository = repository
        self._saq_queue = saq_queue
        self._task_settings = task_settings

    async def get_story(self, id_: int) -> StoryOutDTO:
        story = await self._repository.get_by_id(id_)
        return StoryOutDTO.from_entity(story)

    async def get_all_stories(self) -> list[StoryOutDTO]:
        stories = await self._repository.get_all()
        return [StoryOutDTO.from_entity(story) for story in stories]

    async def create_story(self, dto: StoryCreateDTO) -> StoryOutDTO:
        entity = StoryEntity(
            name=dto.name,
            story_type=dto.story_type,
            delay=dto.delay,
            is_disabled=dto.is_disabled,
            is_blocking=dto.is_blocking,
            is_preview=dto.is_preview,
            is_repetitive=dto.is_repetitive,
            is_autoscroll=dto.is_autoscroll,
            publication_start_time=dto.publication_start_time,
            publication_end_time=dto.publication_end_time,
            created_at=None,
            modified_at=None,
            pages=[],
        )
        story = await self._repository.add(entity)
        return StoryOutDTO.from_entity(story)

    async def update_story(self, dto: StoryUpdateDTO) -> StoryOutDTO:
        entity = await self._repository.get_by_id(dto.id)

        entity.name = dto.name
        entity.story_type = dto.story_type
        entity.delay = dto.delay
        entity.is_disabled = dto.is_disabled
        entity.is_blocking = dto.is_blocking
        entity.is_preview = dto.is_preview
        entity.is_repetitive = dto.is_repetitive
        entity.is_autoscroll = dto.is_autoscroll
        entity.publication_start_time = dto.publication_start_time
        entity.publication_end_time = dto.publication_end_time

        story = await self._repository.update(entity)
        return StoryOutDTO.from_entity(story)

    async def delete_story(self, id_: int) -> None:
        await self._repository.remove_by_id(id_)
