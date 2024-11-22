from typing import Any, Required

import msgspec.json
import saq
from aioinject import Container
from saq.types import Context

from app.config import settings


class TaskContext(Context, total=False):
    container: Required[Container]


class SaqQueue(saq.Queue):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault('dump', msgspec.json.encode)
        kwargs.setdefault('load', msgspec.json.decode)
        kwargs.setdefault('name', settings.task.WORKER_NAME)
        super().__init__(*args, **kwargs)

    def namespace(self, key: str) -> str:
        return f'{settings.app.NAME}:{self.name}:{key}'


saq_queue = SaqQueue.from_url(str(settings.task.REDIS_HOST))
