import logging
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from app.rest_api.jsonapi import (
    JSONApiError,
    JSONApiErrors,
    JSONApiHTTPException,
    get_pointer_field,
)
from app.rest_api.responses import ORJSONResponse
from app.seedwork.domain.exceptions import (
    BusinessLogicError,
    DomainException,
    EntityNotFoundException,
)


__all__ = [
    'register_exception_handlers',
]

logger = logging.getLogger(__name__)


# todo: fix type ignore after https://github.com/encode/starlette/discussions/2416
def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_to_jsonapi_exception,  # type: ignore
    )
    app.add_exception_handler(JSONApiHTTPException, handle_jsonapi_http_exception)  # type: ignore
    app.add_exception_handler(RequestValidationError, handle_request_validation_error)  # type: ignore
    app.add_exception_handler(DomainException, handle_domain_exception)  # type: ignore
    app.add_exception_handler(BusinessLogicError, handle_business_logic_error)  # type: ignore
    app.add_exception_handler(EntityNotFoundException, entity_not_found_handler)  # type: ignore


async def http_exception_to_jsonapi_exception(
    _: Request,
    exc: StarletteHTTPException,
) -> ORJSONResponse:
    errors = JSONApiErrors(
        errors=[
            JSONApiError(
                status=str(exc.status_code),
                detail=exc.detail,
            ),
        ],
    )
    return ORJSONResponse(
        errors.model_dump(exclude_unset=True, exclude_none=True),
        status_code=exc.status_code,
        headers=exc.headers,
    )


async def handle_jsonapi_http_exception(
    _: Request,
    exc: JSONApiHTTPException,
) -> ORJSONResponse:
    return ORJSONResponse(
        content=exc.errors.model_dump(exclude_unset=True, exclude_none=True),
        status_code=exc.status_code,
    )


async def handle_request_validation_error(
    _: Request,
    exc: RequestValidationError,
) -> ORJSONResponse:
    status_code = HTTPStatus.BAD_REQUEST
    errors = JSONApiErrors(
        errors=[
            JSONApiError(
                status=str(status_code),
                code=e.get('type'),
                detail=e.get('msg'),
                source=get_pointer_field(loc) if (loc := e.get('loc')) else None,
            )
            for e in exc.errors()
        ],
    )
    return ORJSONResponse(
        content=errors.model_dump(exclude_unset=True, exclude_none=True),
        status_code=status_code.value,
    )


async def handle_domain_exception(
    _: Request,
    exc: DomainException,
) -> ORJSONResponse:
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    errors = JSONApiErrors(
        errors=[
            JSONApiError(
                status=str(status_code),
                code='domain_error',
                detail=str(exc) or status_code.description,
            ),
        ],
    )
    return ORJSONResponse(
        errors.model_dump(exclude_unset=True, exclude_none=True),
        status_code=status_code.value,
    )


async def handle_business_logic_error(
    _: Request,
    exc: BusinessLogicError[Any],
) -> ORJSONResponse:
    status_code = HTTPStatus.CONFLICT
    errors = JSONApiErrors(
        errors=[
            JSONApiError(
                status=str(status_code),
                code=str(exc.code),
                detail=str(exc),
            ),
        ],
    )
    return ORJSONResponse(
        errors.model_dump(exclude_unset=True, exclude_none=True),
        status_code=status_code.value,
    )


def entity_not_found_handler(_: Request, exc: EntityNotFoundException) -> ORJSONResponse:
    status_code = HTTPStatus.NOT_FOUND
    errors = JSONApiErrors(
        errors=[
            JSONApiError(
                status=str(status_code),
                code='repository_error',
                detail=str(exc),
            ),
        ],
    )
    return ORJSONResponse(
        errors.model_dump(exclude_unset=True, exclude_none=True),
        status_code=status_code.value,
    )
