from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class TrendItem(BaseModel):
    title: str
    description: str = ""
    source: str = ""
    trend_score: float = 0.0
    search_volume: Optional[int] = None
    category: str = ""
    url: str = ""
    keywords: list[str] = []


class TrendResearchModuleInterface(ModuleInterface[Any]):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="trend_discovery",
                description="Discover trending topics across platforms",
                supported_providers=["google_trends", "tiktok", "youtube", "twitter", "reddit"],
            ),
            ModuleCapability(
                name="trend_analysis",
                description="Analyze trend momentum and predict future trends",
            ),
        ]

    @abstractmethod
    async def discover_trends(self, platform: str, category: Optional[str] = None, limit: int = 20) -> list[TrendItem]:
        ...

    @abstractmethod
    async def analyze_trend(self, trend_id: str) -> TrendItem:
        ...

    @abstractmethod
    async def get_trending_categories(self, platform: str) -> list[str]:
        ...

    @abstractmethod
    async def search_trends(self, query: str, platform: Optional[str] = None) -> list[TrendItem]:
        ...
