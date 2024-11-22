from typing import Any

import sentry_sdk
from log_utils import setup_log_utils
from log_utils.configuration.envs import LOG_BASE_HANDLERS

from app.seedwork.utils.types import DictStrAny


__all__ = [
    'configure_logging',
    'configure_sentry',
]


def configure_logging(
    app_name: str,
    app_version: str,
    loggers_overrides: dict[str, Any] | None = None,
    config_overrides: DictStrAny | None = None,
) -> None:
    loggers = {
        'backoff': {
            'handlers': LOG_BASE_HANDLERS,
            'propagate': False,
        },
    }

    if loggers_overrides:
        loggers.update(loggers_overrides)

    setup_log_utils(
        app_name=app_name,
        app_version=app_version,
        include_traceback=True,
        framework='starlette',
        loggers=loggers,
        **(config_overrides or {}),
    )


def configure_sentry(
    dsn: str,
    environment: str,
    traces_sample_rate: float = 0.1,
) -> None:
    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=traces_sample_rate,
        environment=environment,
        send_default_pii=True,
    )
