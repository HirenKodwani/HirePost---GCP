from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ConfigProviderInterface, ModuleCapability, ModuleInterface, ModuleStatus


class ConfigurationModuleInterface(ModuleInterface[Any]):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="configuration",
                description="Manage application configuration",
                supported_providers=["file", "env", "database"],
            )
        ]

    @abstractmethod
    async def get(self, key: str, default: Optional[Any] = None) -> Any:
        ...

    @abstractmethod
    async def set(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    async def get_all(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def reload(self) -> None:
        ...

    @abstractmethod
    async def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        ...

    @abstractmethod
    async def export(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def import_config(self, config: dict[str, Any]) -> None:
        ...
