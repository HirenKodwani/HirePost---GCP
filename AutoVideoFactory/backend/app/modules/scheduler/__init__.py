from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class ScheduledJob(BaseModel):
    id: str = ""
    job_type: str = ""
    params: dict = {}
    scheduled_at: Optional[datetime] = None
    repeat: Optional[str] = None
    status: str = "pending"
    priority: int = 0


class SchedulerModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="job_scheduling",
                description="Schedule and manage content generation jobs",
            ),
        ]

    @abstractmethod
    async def schedule(self, job_type: str, params: dict, scheduled_at: Optional[datetime] = None, repeat: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def cancel(self, job_id: str) -> bool:
        ...

    @abstractmethod
    async def list_jobs(self, status: Optional[str] = None) -> list[ScheduledJob]:
        ...

    @abstractmethod
    async def pause(self) -> None:
        ...

    @abstractmethod
    async def resume(self) -> None:
        ...

    @abstractmethod
    async def get_status(self) -> dict:
        ...
