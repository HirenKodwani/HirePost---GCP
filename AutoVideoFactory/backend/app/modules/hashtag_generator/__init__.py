from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class HashtagSet(BaseModel):
    hashtags: list[str] = []
    category: str = ""
    estimated_reach: int = 0
    platform: str = "tiktok"


class HashtagGeneratorModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="hashtag_generation",
                description="Generate optimized hashtags for platform reach",
                supported_providers=["llm", "trending"],
            ),
        ]

    @abstractmethod
    async def generate_hashtags(self, topic: str, platform: str = "tiktok", count: int = 10) -> HashtagSet:
        ...

    @abstractmethod
    async def analyze_hashtag(self, hashtag: str, platform: str = "tiktok") -> dict:
        ...

    @abstractmethod
    async def get_trending_hashtags(self, platform: str, category: Optional[str] = None) -> list[str]:
        ...
