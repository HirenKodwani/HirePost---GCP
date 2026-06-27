from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ContentGenerationProviderInterface, ModuleCapability, ModuleInterface


class VideoGenerationResult(BaseModel):
    file_path: str
    duration_seconds: float = 0.0
    width: int = 0
    height: int = 0
    fps: float = 30.0
    provider: str = ""
    prompt_used: str = ""


class VideoGenerationModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="video_generation",
                description="Generate videos from text/image prompts",
                supported_providers=["kling", "hailuo", "runway", "luma", "wan"],
            ),
            ModuleCapability(
                name="video_provider_abstraction",
                description="Interchangeable video generation providers",
            ),
        ]

    @abstractmethod
    async def generate_from_prompt(self, prompt: str, **kwargs) -> VideoGenerationResult:
        ...

    @abstractmethod
    async def generate_from_image(self, image_path: str, prompt: str, **kwargs) -> VideoGenerationResult:
        ...

    @abstractmethod
    async def get_progress(self, task_id: str) -> dict:
        ...

    @abstractmethod
    async def list_providers(self) -> list[dict]:
        ...
