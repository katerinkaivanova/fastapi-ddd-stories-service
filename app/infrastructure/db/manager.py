from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import database


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    def init(self, db_dsn: URL) -> None:
        self._engine = create_async_engine(
            db_dsn,
            echo=database.ECHO,
            pool_size=database.POOL_MIN_SIZE,
            max_overflow=database.POOL_MAX_SIZE,
            pool_timeout=database.POOL_TIMEOUT,
            pool_pre_ping=database.POOL_PRE_PING,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,  # don't expire objects after transaction commit
        )

    async def close(self) -> None:
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._session_factory = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_factory is None:
            msg = 'DatabaseSessionManager is not initialized'
            raise OSError(msg)
        async with self._session_factory.begin() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            msg = 'DatabaseSessionManager is not initialized'
            raise OSError(msg)
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager = DatabaseSessionManager()
