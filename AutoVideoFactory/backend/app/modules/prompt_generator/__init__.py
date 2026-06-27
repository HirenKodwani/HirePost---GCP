from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class PromptOutput(BaseModel):
    prompt_type: str
    original_text: str
    optimized_text: Optional[str] = None
    parameters: dict[str, Any] = {}
    provider: str = ""
    quality_score: float = 0.0


class PromptGeneratorModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="prompt_generation",
                description="Generate prompts for AI models (image, video, voice)",
                supported_providers=["llm", "template"],
            ),
            ModuleCapability(
                name="multi_modal_prompt",
                description="Generate prompts for different AI modalities",
            ),
        ]

    @abstractmethod
    async def generate_image_prompt(self, scene_description: str, style: Optional[str] = None) -> PromptOutput:
        ...

    @abstractmethod
    async def generate_video_prompt(self, scene_description: str, duration: float = 5.0) -> PromptOutput:
        ...

    @abstractmethod
    async def generate_voice_prompt(self, script_text: str, voice_style: Optional[str] = None) -> PromptOutput:
        ...

    @abstractmethod
    async def generate_music_prompt(self, mood: str, genre: Optional[str] = None, duration: float = 30.0) -> PromptOutput:
        ...
