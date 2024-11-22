from fastapi import FastAPI
from fastapi.openapi.models import Contact
from fastapi.openapi.utils import get_openapi

from app.config import settings
from app.seedwork.utils.types import DictStrAny


def custom_openapi(app: FastAPI) -> DictStrAny:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.openapi.TITLE,
        version=settings.openapi.VERSION,
        description=settings.openapi.DESCRIPTION,
        contact=Contact(name=settings.openapi.CONTACT_NAME).model_dump(),
        routes=app.routes,
    )
    # hack: remove hardcoded 422 response
    # see also: https://github.com/tiangolo/fastapi/issues/660
    for path in openapi_schema['paths'].values():
        for method_data in path.values():
            response_422 = method_data['responses'].get('422')
            if response_422 and response_422['description'] == 'Validation Error':
                del method_data['responses']['422']

    app.openapi_schema = openapi_schema
    return app.openapi_schema
