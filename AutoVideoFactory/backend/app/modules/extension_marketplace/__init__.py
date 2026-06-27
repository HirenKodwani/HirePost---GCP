from __future__ import annotations

from abc import abstractmethod

from ..base import ModuleCapability, ModuleInterface


class ExtensionMarketplaceModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="extension_marketplace",
                description="Browse, install, and manage extensions",
            ),
        ]

    @abstractmethod
    async def search(self, query: str) -> list[dict]:
        ...

    @abstractmethod
    async def install(self, extension_id: str) -> bool:
        ...

    @abstractmethod
    async def uninstall(self, extension_id: str) -> bool:
        ...

    @abstractmethod
    async def list_installed(self) -> list[dict]:
        ...

    @abstractmethod
    async def check_updates(self) -> list[dict]:
        ...

    @abstractmethod
    async def update(self, extension_id: str) -> bool:
        ...
