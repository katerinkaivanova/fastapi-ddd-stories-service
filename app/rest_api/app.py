from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from aioinject import Container
from fastapi import FastAPI
from starlette.types import Lifespan

from app.config import settings
from app.di.container import create_container
from app.infrastructure.db import db_manager
from app.infrastructure.logging import configure_logging
from app.rest_api.exception_handlers import register_exception_handlers
from app.rest_api.middlewares import register_middlewares
from app.rest_api.openapi import custom_openapi
from app.rest_api.responses import ORJSONResponse, default_json_responses
from app.rest_api.routes import register_routes


def create_lifespan(container: Container) -> Lifespan[FastAPI]:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        # startup
        db_manager.init(settings.database.dsn())
        yield
        # shutdown
        await db_manager.close()
        await container.aclose()

    return lifespan


def create_app(**kwargs: Any) -> FastAPI:
    configure_logging()

    container = create_container()
    app = FastAPI(
        debug=settings.app.DEBUG,
        lifespan=create_lifespan(container),
        default_response_class=ORJSONResponse,
        responses=default_json_responses,
        openapi_url='/docs/oss/openapi.json',
        docs_url='/docs/oss/',
        redoc_url=None,
        **kwargs,
    )

    register_routes(app)
    register_middlewares(app, container)
    register_exception_handlers(app)

    app.openapi_schema = custom_openapi(app)

    return app
