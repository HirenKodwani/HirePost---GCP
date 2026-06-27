from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

import httpx

from ..core.exceptions import ProviderError
from ..core.logging import get_logger

logger = get_logger("autovideofactory.services.stock")


class StockProvider(ABC):
    provider_name: str = "base"

    @abstractmethod
    async def search_videos(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def search_images(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        ...


class PexelsProvider(StockProvider):
    provider_name = "pexels"

    def __init__(self, api_key: str = "") -> None:
        self._api_key = api_key or ""
        self._http = httpx.AsyncClient()

    async def search_videos(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        try:
            headers = {"Authorization": self._api_key} if self._api_key else {}
            response = await self._http.get(
                "https://api.pexels.com/videos/search",
                params={"query": query, "per_page": max_results},
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "url": v.get("url", ""),
                    "source": "pexels",
                    "duration": v.get("duration", 0),
                    "width": v.get("width", 0),
                    "height": v.get("height", 0),
                    "files": v.get("video_files", []),
                }
                for v in data.get("videos", [])
            ]
        except Exception as e:
            logger.warning(f"Pexels search failed: {e}")
            return []

    async def search_images(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        return []


class PixabayProvider(StockProvider):
    provider_name = "pixabay"

    def __init__(self, api_key: str = "") -> None:
        self._api_key = api_key or ""
        self._http = httpx.AsyncClient()

    async def search_videos(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        try:
            params = {"q": query, "per_page": max_results, "safesearch": "true"}
            if self._api_key:
                params["key"] = self._api_key
            response = await self._http.get("https://pixabay.com/api/videos/", params=params)
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "url": v.get("pageURL", ""),
                    "source": "pixabay",
                    "duration": v.get("duration", 0),
                    "tags": v.get("tags", ""),
                    "videos": v.get("videos", {}),
                }
                for v in data.get("hits", [])
            ]
        except Exception as e:
            logger.warning(f"Pixabay search failed: {e}")
            return []

    async def search_images(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        return []


class StockProviderRegistry:
    _providers: dict[str, type[StockProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[StockProvider]) -> None:
        cls._providers[name] = provider_class

    @classmethod
    def get(cls, name: str) -> StockProvider:
        provider_class = cls._providers.get(name)
        if not provider_class:
            raise ProviderError(f"Unknown stock provider: {name}", provider_name=name)
        return provider_class()

    @classmethod
    def list_providers(cls) -> list[dict[str, str]]:
        return [{"name": n, "class": p.__name__} for n, p in cls._providers.items()]


StockProviderRegistry.register("pexels", PexelsProvider)
StockProviderRegistry.register("pixabay", PixabayProvider)
