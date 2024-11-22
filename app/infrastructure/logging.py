from functools import cache

from app.config import settings
from app.seedwork.infrastructure import logging
from app.seedwork.infrastructure.exceptions import ImproperlyConfigured
from app.version import VERSION


@cache
def configure_logging() -> None:
    logging.configure_logging(
        app_name=settings.app.NAME,
        app_version=VERSION,
        config_overrides={
            'raise_on_log_exceptions': settings.app.RAISE_ON_LOG_EXCEPTIONS,
        },
    )

    if settings.sentry.ENABLED:  # pragma: no cover
        if not (dsn := settings.sentry.DSN):
            msg = 'Sentry mode enabled but DSN not set'
            raise ImproperlyConfigured(msg)

        logging.configure_sentry(
            dsn=dsn,
            traces_sample_rate=settings.sentry.TRACES_SAMPLE_RATE,
            environment=settings.sentry.STAGE_NAME,
        )
