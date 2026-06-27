from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from .config import settings
from .logging import get_logger
from ..models.base import Base
from ..models import *  # noqa: F401, F403 - register all models

logger = get_logger("autovideofactory.database")


class DatabaseEngine:
    _engine = None
    _session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            db_url = settings.database_url
            logger.info("Initializing database", extra={"url": db_url})
            cls._engine = create_async_engine(
                db_url,
                echo=settings.database_echo,
                pool_size=settings.database_pool_size,
                max_overflow=settings.database_max_overflow,
            )
        return cls._engine

    @classmethod
    def get_session_factory(cls) -> async_sessionmaker[AsyncSession]:
        if cls._session_factory is None:
            cls._session_factory = async_sessionmaker(
                cls.get_engine(),
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return cls._session_factory

    @classmethod
    async def create_all(cls) -> None:
        async with cls.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

    @classmethod
    async def dispose(cls) -> None:
        if cls._engine:
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
        logger.info("Database engine disposed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    factory = DatabaseEngine.get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
