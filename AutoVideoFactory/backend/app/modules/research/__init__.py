from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class ResearchResult(BaseModel):
    topic: str
    summary: str = ""
    key_points: list[str] = []
    facts: list[dict] = []
    sources: list[str] = []
    statistics: list[dict] = []
    related_topics: list[str] = []


class ResearchModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="web_research",
                description="Research topics using web search and AI",
                supported_providers=["web", "llm", "browser"],
            ),
            ModuleCapability(
                name="fact_checking",
                description="Verify facts and claims automatically",
            ),
        ]

    @abstractmethod
    async def research_topic(self, topic: str, depth: str = "standard") -> ResearchResult:
        ...

    @abstractmethod
    async def research_with_browser(self, topic: str, url: Optional[str] = None) -> ResearchResult:
        ...

    @abstractmethod
    async def fact_check(self, claims: list[str]) -> list[dict]:
        ...

    @abstractmethod
    async def extract_insights(self, text: str) -> dict:
        ...
