from __future__ import annotations

from abc import abstractmethod
from typing import Any

from ..base import ModuleCapability, ModuleInterface


class NotificationModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="notifications",
                description="Send system notifications via various channels",
                supported_providers=["desktop", "web", "email", "slack", "discord"],
            ),
        ]

    @abstractmethod
    async def send(self, title: str, message: str, channel: str = "desktop", data: dict | None = None) -> bool:
        ...

    @abstractmethod
    async def broadcast(self, title: str, message: str, channels: list[str] | None = None) -> dict[str, bool]:
        ...

    @abstractmethod
    async def get_history(self, limit: int = 50) -> list[dict]:
        ...
