from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class ImageGenerationResult(BaseModel):
    file_path: str
    width: int = 0
    height: int = 0
    prompt_used: str = ""
    provider: str = ""
    seed: Optional[int] = None


class ImageGenerationModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="image_generation",
                description="Generate images from text prompts",
                supported_providers=["pollinations", "stability", "sd", "openai", "comfyui"],
            ),
            ModuleCapability(
                name="image_variation",
                description="Generate variations of existing images",
            ),
        ]

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> ImageGenerationResult:
        ...

    @abstractmethod
    async def generate_variation(self, image_path: str, prompt: str, **kwargs) -> ImageGenerationResult:
        ...

    @abstractmethod
    async def upscale(self, image_path: str, scale: int = 2) -> str:
        ...

    @abstractmethod
    async def inpaint(self, image_path: str, mask_path: str, prompt: str) -> str:
        ...
