from collections.abc import Sequence
from typing import Self, cast

from pydantic import ConfigDict
from pydantic_core import ErrorDetails
from starlette import status

from app.rest_api.utils import SchemaModel
from app.seedwork.utils.types import DictStrAny


class JSONApiErrorSource(SchemaModel):
    pointer: str | None = None
    parameter: str | None = None
    header: str | None = None


class JSONApiError(SchemaModel):
    """Describe of a single error object specified in JSONApiErrors.

    The format of all fields corresponds to spec: https://jsonapi.org/format/1.1/#errors

    """

    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: str | None = None
    links: DictStrAny | None = None
    status: str | None = None
    code: str | None = None
    title: str | None = None
    detail: str | None = None
    source: JSONApiErrorSource | None = None
    meta: DictStrAny | None = None


class JSONApiErrors(SchemaModel):
    """JSON:API spec error object.

    See Also: https://jsonapi.org/format/1.1/#errors

    """

    errors: Sequence[JSONApiError]

    @classmethod
    def from_validation_errors(
        cls,
        errors: Sequence[ErrorDetails],
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        title: str | None = None,
    ) -> Self:
        return cls(
            errors=[
                JSONApiError(
                    status=str(status_code),
                    title=title,
                    code=e.get('type'),
                    detail=e.get('msg'),
                    source=get_pointer_field(loc) if (loc := e.get('loc')) else None,
                )
                for e in errors
            ],
        )


def get_pointer_field(loc: tuple[int | str, ...]) -> JSONApiErrorSource | None:
    if len(loc) < 2 or (len(loc) == 2 and isinstance(loc[1], int)):  # noqa: PLR2004
        return None

    loc = cast(tuple[str, ...], loc)

    attrs: dict[str, str] = {}
    if loc[0] == 'body':
        attrs['pointer'] = '/' + '/'.join(map(str, loc[1:]))
    elif loc[0] == 'query':
        attrs['parameter'] = loc[1]
    elif loc[0] == 'header':
        attrs['header'] = loc[1]

    return JSONApiErrorSource(**attrs) if attrs else None


class JSONApiHTTPException(Exception):
    def __init__(
        self,
        errors: JSONApiErrors,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: dict[str, str] | None = None,
    ):
        self.errors = errors
        self.status_code = status_code
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(status_code={self.status_code!r})'
