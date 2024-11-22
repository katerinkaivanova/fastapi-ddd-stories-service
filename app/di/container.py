from collections.abc import Iterable
from functools import cache
from itertools import chain
from typing import Any

from aioinject import Container
from aioinject.providers import Provider

from app import infrastructure
from app.modules import story


__all__ = ['create_container']

_modules: Iterable[Iterable[Provider[Any]]] = (
    infrastructure.providers,
    story.providers,
)


@cache
def create_container() -> Container:
    container = Container()

    for provider in chain.from_iterable(_modules):
        container.register(provider)

    return container
