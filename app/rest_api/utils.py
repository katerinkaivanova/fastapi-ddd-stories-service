import datetime

from pydantic import BaseModel, ConfigDict

from app.seedwork.utils.dt import iso8601_duration_format


class SchemaModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        coerce_numbers_to_str=True,
        json_encoders={datetime.timedelta: iso8601_duration_format},
    )


def to_kebab_case(value: str) -> str:
    return value.replace('_', '-')


class KebabCaseModel(SchemaModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_kebab_case,
    )


def to_camel_case(value: str) -> str:
    camel_case_value = ''.join(
        w.lower() if i == 0 else w.title()
        for i, w in enumerate(value.strip('_').split('_'))
    )
    if value.startswith('_'):
        camel_case_value = f'_{camel_case_value}'

    return camel_case_value


class CamelCaseModel(SchemaModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel_case,
    )
