from fastapi import APIRouter

from app.rest_api.manager.story.views import router as story_router


__all__ = ['manager_router']

manager_router = APIRouter(prefix='/manager')
manager_router.include_router(story_router)
