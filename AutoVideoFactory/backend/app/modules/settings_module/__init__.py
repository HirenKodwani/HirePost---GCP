from __future__ import annotations

from abc import abstractmethod
from typing import Any

from ..base import ModuleCapability, ModuleInterface
from ...core.config import Settings


class SettingsModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="settings_management",
                description="Manage application settings via UI and API",
            ),
        ]

    @abstractmethod
    async def get_all(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get_section(self, section: str) -> dict[str, Any]:
        ...

    @abstractmethod
    async def update(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    async def reset(self, key: str) -> None:
        ...

    @abstractmethod
    async def validate(self, settings: dict[str, Any]) -> list[str]:
        ...

    @abstractmethod
    async def export(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def import_settings(self, data: dict[str, Any]) -> int:
        ...
