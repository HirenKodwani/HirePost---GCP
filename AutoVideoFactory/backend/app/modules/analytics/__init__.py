from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class VideoAnalytics(BaseModel):
    video_id: str = ""
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    watch_time_seconds: float = 0.0
    avg_watch_percentage: float = 0.0
    follower_growth: int = 0
    platform: str = ""


class AnalyticsModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="analytics_collection",
                description="Collect and analyze video performance data",
                supported_providers=["browser", "api", "web"],
            ),
            ModuleCapability(
                name="performance_insights",
                description="Generate insights from analytics data",
            ),
        ]

    @abstractmethod
    async def track_event(self, event_type: str, data: dict) -> None:
        ...

    @abstractmethod
    async def get_video_stats(self, video_id: str, platform: str) -> VideoAnalytics:
        ...

    @abstractmethod
    async def get_browser_stats(self, video_url: str, platform: str) -> VideoAnalytics:
        ...

    @abstractmethod
    async def generate_report(self, video_ids: list[str], period: str = "7d") -> dict:
        ...

    @abstractmethod
    async def compare_performance(self, video_ids: list[str]) -> list[dict]:
        ...
