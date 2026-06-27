from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class PublishResult(BaseModel):
    success: bool = False
    platform: str = ""
    video_url: str = ""
    published_at: str = ""
    views: int = 0
    error: Optional[str] = None


class PublisherModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="video_publishing",
                description="Publish videos to social media platforms",
                supported_providers=["youtube", "tiktok", "instagram", "twitter", "linkedin", "facebook"],
            ),
            ModuleCapability(
                name="browser_publishing",
                description="Publish using browser automation when APIs unavailable",
            ),
        ]

    @abstractmethod
    async def publish(self, video_path: str, metadata: dict, platform: str) -> PublishResult:
        ...

    @abstractmethod
    async def publish_browser(self, video_path: str, metadata: dict, platform: str) -> PublishResult:
        ...

    @abstractmethod
    async def schedule_publish(self, video_path: str, metadata: dict, platform: str, publish_at: str) -> PublishResult:
        ...

    @abstractmethod
    async def check_status(self, publish_id: str, platform: str) -> dict:
        ...

    @abstractmethod
    async def list_platforms(self) -> list[dict]:
        ...
