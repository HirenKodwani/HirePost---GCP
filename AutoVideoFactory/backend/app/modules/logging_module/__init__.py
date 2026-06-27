from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional

from ..base import ModuleCapability, ModuleInterface


class LogEntry:
    timestamp: datetime
    level: str
    logger: str
    message: str
    extra: dict[str, Any] = {}


class LoggingModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="log_management",
                description="Centralized log collection and querying",
            ),
            ModuleCapability(
                name="log_streaming",
                description="Real-time log streaming for UI",
            ),
        ]

    @abstractmethod
    async def query(self, level: Optional[str] = None, logger_name: Optional[str] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, limit: int = 100) -> list[LogEntry]:
        ...

    @abstractmethod
    async def stream(self, callback, level: Optional[str] = None) -> None:
        ...

    @abstractmethod
    async def get_stats(self) -> dict:
        ...

    @abstractmethod
    async def clear(self, before: Optional[datetime] = None) -> int:
        ...
