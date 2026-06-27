from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class QAReport(BaseModel):
    passed: bool = False
    issues: list[dict] = []
    score: float = 0.0
    details: dict = {}
    recommendations: list[str] = []


class QualityAssuranceModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="video_qa",
                description="Automated quality checks on generated videos",
                supported_providers=["ffmpeg", "opencv", "llm"],
            ),
        ]

    @abstractmethod
    async def review_video(self, video_path: str) -> QAReport:
        ...

    @abstractmethod
    async def check_audio(self, video_path: str) -> dict:
        ...

    @abstractmethod
    async def check_visual(self, video_path: str) -> dict:
        ...

    @abstractmethod
    async def check_content(self, script: str, video_path: str) -> dict:
        ...

    @abstractmethod
    async def validate_output(self, expected: dict, actual: dict) -> QAReport:
        ...
