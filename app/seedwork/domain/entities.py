from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar


__all__ = [
    'Entity',
    'EntityT',
    'EntityId',
]


EntityId = TypeVar('EntityId', bound=int)


@dataclass(kw_only=True)
class Entity(Generic[EntityId]):
    """Base class for domain (business) entities."""

    id: EntityId = field(default=1, hash=True)  # type: ignore


EntityT = TypeVar('EntityT', bound=Entity[Any])
