from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class ThumbnailResult(BaseModel):
    file_path: str
    width: int = 0
    height: int = 0
    prompt_used: str = ""
    click_prediction: float = 0.0


class ThumbnailGenerationModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="thumbnail_generation",
                description="Generate eye-catching video thumbnails",
                supported_providers=["image_gen", "template", "composite"],
            ),
            ModuleCapability(
                name="a_b_thumbnail_testing",
                description="Generate and score multiple thumbnail variations",
            ),
        ]

    @abstractmethod
    async def generate_from_video(self, video_path: str, timestamp: Optional[float] = None) -> ThumbnailResult:
        ...

    @abstractmethod
    async def generate_from_prompt(self, prompt: str, style: Optional[str] = None) -> ThumbnailResult:
        ...

    @abstractmethod
    async def generate_variations(self, video_path: str, count: int = 3) -> list[ThumbnailResult]:
        ...

    @abstractmethod
    async def add_text_overlay(self, thumbnail_path: str, title: str) -> str:
        ...
