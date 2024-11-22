from fastapi import APIRouter

from app.seedwork.utils.types import DictStrAny
from app.version import VERSION


router = APIRouter(prefix='/internal', tags=['internal'])


@router.get('/oss/get-component-version/', response_model=None)
def get_component_version() -> DictStrAny:
    return {'data': {'version': VERSION}}
