from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class TitleResult(BaseModel):
    title: str
    score: float = 0.0
    platform: str = "tiktok"
    style: str = ""


class TitleGeneratorModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="title_generation",
                description="Generate optimized video titles",
                supported_providers=["llm", "template"],
            ),
        ]

    @abstractmethod
    async def generate_titles(self, topic: str, platform: str = "tiktok", count: int = 5) -> list[TitleResult]:
        ...

    @abstractmethod
    async def score_title(self, title: str, platform: str = "tiktok") -> float:
        ...

    @abstractmethod
    async def optimize_for_platform(self, title: str, platform: str) -> str:
        ...
