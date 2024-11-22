from aioinject import Container
from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI
from log_utils.extensions.starlette import log_http_middleware
from starlette.middleware.cors import CORSMiddleware


__all__ = ['register_middlewares']


def register_middlewares(app: FastAPI, container: Container) -> None:
    app.add_middleware(AioInjectMiddleware, container=container)
    app.middleware('http')(log_http_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
