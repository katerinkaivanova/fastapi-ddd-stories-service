from collections.abc import Mapping
from dataclasses import dataclass
from functools import cached_property
from typing import Any, ClassVar, Generic, TypedDict, TypeVar, cast

from app.seedwork.domain.entities import EntityT
from app.seedwork.utils.types import DictStrAny


__all__ = [
    'ErrorContextT',
    'EmptyErrorContext',
    'DomainError',
    'DomainException',
    'BusinessLogicError',
    'EntityNotFoundException',
]


ErrorContextT = TypeVar('ErrorContextT')


@dataclass(frozen=True, slots=True, kw_only=True)
class DomainError:
    code: int
    message: str = ''


class EmptyErrorContext(TypedDict):
    pass


class DomainException(Exception):
    pass


class BusinessLogicError(Generic[ErrorContextT], DomainException):
    error: ClassVar[DomainError]

    def __init__(self, context: ErrorContextT) -> None:
        self.context: ErrorContextT = context

    def __str__(self) -> str:
        return self.message

    @property
    def code(self) -> int:
        return self.error.code

    @cached_property
    def message(self) -> str:
        msg = str(self.error.message)
        context = cast(Mapping[str, Any], self.context)
        return msg.format(**context) if self.context else msg


class EntityNotFoundException(Exception):
    def __init__(self, entity_type: type[EntityT] | str, kwargs: DictStrAny) -> None:
        name = entity_type.__name__ if not isinstance(entity_type, str) else entity_type
        message = f'{name} with {kwargs} not found'
        super().__init__(message)
        self.name = name
        self.kwargs = kwargs
