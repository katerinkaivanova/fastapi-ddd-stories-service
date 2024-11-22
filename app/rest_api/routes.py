from fastapi import APIRouter, FastAPI

from app.rest_api.internal.router import internal_router
from app.rest_api.manager.router import manager_router


__all__ = ['register_routes']


def register_routes(app: FastAPI) -> None:
    api_router = APIRouter(prefix='/api')
    api_router.include_router(manager_router)
    api_router.include_router(internal_router)

    app.include_router(api_router)
