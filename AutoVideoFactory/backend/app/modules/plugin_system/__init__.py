from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import Any

from ..base import ModuleCapability, ModuleInterface


class PluginInfo:
    name: str
    version: str
    description: str
    author: str
    entry_point: str


class PluginSystemModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="plugin_loading",
                description="Dynamically load and manage plugins",
            ),
            ModuleCapability(
                name="plugin_isolation",
                description="Run plugins in isolated environments",
            ),
        ]

    @abstractmethod
    async def discover_plugins(self, directory: Path | None = None) -> list[PluginInfo]:
        ...

    @abstractmethod
    async def load_plugin(self, plugin_name: str) -> bool:
        ...

    @abstractmethod
    async def unload_plugin(self, plugin_name: str) -> bool:
        ...

    @abstractmethod
    async def enable_plugin(self, plugin_name: str) -> bool:
        ...

    @abstractmethod
    async def disable_plugin(self, plugin_name: str) -> bool:
        ...

    @abstractmethod
    async def list_plugins(self) -> list[dict]:
        ...

    @abstractmethod
    async def get_plugin_info(self, plugin_name: str) -> dict | None:
        ...
