from typing import ClassVar

from pydantic_core import ErrorDetails
from starlette import status

from app.rest_api.jsonapi import (
    JSONApiError,
    JSONApiErrors,
)


class JSONApiHTTPError(Exception):
    title: ClassVar[str] = 'Internal Server Error'
    status_code: ClassVar = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        errors: JSONApiErrors,
        headers: dict[str, str] | None = None,
    ):
        self.errors = errors
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}(status_code={self.status_code!r})'


class ResourceNotFoundByIdError(JSONApiHTTPError):
    title = 'Resource not found'
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(
        self,
        resource_type: str,
        resource_id: int,
    ) -> None:
        title = str(self.title)
        detail = f'{resource_type} with id {resource_id} not found'
        errors = JSONApiErrors(
            errors=[
                JSONApiError(
                    status=self.status_code,
                    title=title,
                    detail=str(detail) if detail else title,
                    code='not_found',
                ),
            ],
        )
        super().__init__(errors=errors)


class RequestParamValidationError(JSONApiHTTPError):
    title = 'Parameter validation error'
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, errors: list[ErrorDetails]) -> None:
        title = str(self.title)
        super().__init__(
            errors=JSONApiErrors.from_validation_errors(
                errors=errors,
                status_code=self.status_code,
                title=str(title),
            ),
        )
