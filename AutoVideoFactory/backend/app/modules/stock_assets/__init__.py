from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class StockAssetItem(BaseModel):
    url: str
    thumbnail_url: str = ""
    asset_type: str = "video"
    width: int = 0
    height: int = 0
    duration_seconds: float = 0.0
    license_type: str = "royalty_free"
    source: str = ""
    attribution: str = ""
    download_url: str = ""


class StockAssetModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="stock_search",
                description="Search for royalty-free stock assets",
                supported_providers=["pexels", "pixabay", "coverr"],
            ),
            ModuleCapability(
                name="asset_download",
                description="Download stock assets for local use",
            ),
        ]

    @abstractmethod
    async def search_videos(self, query: str, max_results: int = 10) -> list[StockAssetItem]:
        ...

    @abstractmethod
    async def search_images(self, query: str, max_results: int = 10) -> list[StockAssetItem]:
        ...

    @abstractmethod
    async def download_asset(self, asset: StockAssetItem, output_path: str) -> str:
        ...

    @abstractmethod
    async def search_music(self, query: str, mood: Optional[str] = None, max_results: int = 10) -> list[StockAssetItem]:
        ...
