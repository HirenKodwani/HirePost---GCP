from __future__ import annotations

from abc import abstractmethod

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class ContentScore(BaseModel):
    overall: float = 0.0
    engagement: float = 0.0
    quality: float = 0.0
    relevance: float = 0.0
    originality: float = 0.0
    platform_fit: float = 0.0


class ContentScoringModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="content_scoring",
                description="Score content quality and predicted performance",
            ),
        ]

    @abstractmethod
    async def score_script(self, script: str, platform: str = "tiktok") -> ContentScore:
        ...

    @abstractmethod
    async def score_video(self, video_path: str, metadata: dict) -> ContentScore:
        ...

    @abstractmethod
    async def predict_performance(self, content_score: ContentScore, platform: str = "tiktok") -> dict:
        ...
