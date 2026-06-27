from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class TopicItem(BaseModel):
    title: str
    description: str = ""
    niche: str = ""
    relevance_score: float = 0.0
    competition_level: str = "medium"
    estimated_views: Optional[int] = None
    keywords: list[str] = []


class TopicDiscoveryModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="topic_generation",
                description="Generate video topic ideas based on trends and niches",
            ),
            ModuleCapability(
                name="topic_scoring",
                description="Score and rank topics by potential performance",
            ),
        ]

    @abstractmethod
    async def discover_topics(self, niche: str, count: int = 10) -> list[TopicItem]:
        ...

    @abstractmethod
    async def score_topic(self, topic: TopicItem) -> TopicItem:
        ...

    @abstractmethod
    async def find_gaps(self, niche: str) -> list[TopicItem]:
        ...

    @abstractmethod
    async def validate_topic(self, title: str) -> dict:
        ...
