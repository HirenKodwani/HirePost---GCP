from __future__ import annotations

from abc import abstractmethod
from typing import Any

from ..base import ModuleCapability, ModuleInterface


class DashboardModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="dashboard_data",
                description="Aggregate data for dashboard display",
            ),
            ModuleCapability(
                name="real_time_stats",
                description="Real-time system statistics streaming",
            ),
        ]

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get_queue_status(self) -> dict:
        ...

    @abstractmethod
    async def get_agent_status(self) -> list[dict]:
        ...

    @abstractmethod
    async def get_recent_jobs(self, limit: int = 10) -> list[dict]:
        ...

    @abstractmethod
    async def get_system_resources(self) -> dict:
        ...
