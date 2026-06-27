from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class SEOAnalysis(BaseModel):
    title_score: float = 0.0
    description_score: float = 0.0
    hashtag_score: float = 0.0
    overall_score: float = 0.0
    suggestions: list[str] = []


class SEOOptimizerModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="seo_analysis",
                description="Analyze and optimize content for search discovery",
                supported_providers=["llm", "rules"],
            ),
        ]

    @abstractmethod
    async def analyze(self, title: str, description: str, hashtags: list[str], platform: str = "youtube") -> SEOAnalysis:
        ...

    @abstractmethod
    async def optimize_title(self, title: str, platform: str = "youtube") -> str:
        ...

    @abstractmethod
    async def optimize_description(self, description: str, platform: str = "youtube", keywords: Optional[list[str]] = None) -> str:
        ...

    @abstractmethod
    async def suggest_keywords(self, topic: str, platform: str = "youtube") -> list[str]:
        ...
