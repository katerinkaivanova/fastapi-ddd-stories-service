from typing import Any, Final, Generic, TypeAlias, TypeVar

import orjson
from fastapi.responses import JSONResponse as DefaultJSONResponse
from pydantic import BaseModel

from app.rest_api.errors import JSONApiHTTPError
from app.rest_api.jsonapi import JSONApiErrors


__all__ = [
    'Response',
    'ListResponse',
    'ORJSONResponse',
    'build_responses',
    'default_json_responses',
    'JSON_MEDIA_TYPE',
    'JSON_API_MEDIA_TYPE',
]

JSON_MEDIA_TYPE: Final = 'application/json'
JSON_API_MEDIA_TYPE: Final = 'application/vnd.api+json'

DataT = TypeVar('DataT')


_Responses: TypeAlias = dict[int | str, dict[str, Any]] | None

default_json_responses: Final[_Responses] = {400: {'model': JSONApiErrors}}


class ORJSONResponse(DefaultJSONResponse):
    option = orjson.OPT_UTC_Z | orjson.OPT_NON_STR_KEYS

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=self.option)


class JSONApiResponse(ORJSONResponse):
    media_type = JSON_API_MEDIA_TYPE


class _BaseResponse(BaseModel):
    pass


class Response(_BaseResponse, Generic[DataT]):
    data: DataT


class ListResponse(_BaseResponse, Generic[DataT]):
    data: list[DataT]


def build_responses(
    status_code: int,
    response_model: type[BaseModel] | None,
    exceptions: tuple[type[JSONApiHTTPError], ...] = (),
    content_type: str = JSON_MEDIA_TYPE,
) -> dict[int | str, dict[str, Any]] | None:
    model_schema = response_model.model_json_schema() if response_model else None
    return {
        status_code: {
            'content': {content_type: model_schema},
        },
        **{
            exception.status_code: {
                'content': {content_type: JSONApiErrors.model_json_schema()},
            }
            for exception in exceptions
        },
    }
