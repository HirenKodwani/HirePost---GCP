from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class ScenePlan(BaseModel):
    scene_number: int
    description: str
    duration_seconds: float = 10.0
    visual_notes: str = ""
    audio_notes: str = ""
    transition: str = "cut"


class ScriptOutput(BaseModel):
    title: str
    content: str
    scenes: list[ScenePlan] = []
    word_count: int = 0
    estimated_duration: float = 0.0
    tone: str = "neutral"
    hook: str = ""
    call_to_action: str = ""


class ScriptWriterModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="script_generation",
                description="Generate video scripts from research data",
                supported_providers=["llm", "template"],
            ),
            ModuleCapability(
                name="scene_planning",
                description="Break scripts into visual scenes",
            ),
        ]

    @abstractmethod
    async def generate_script(self, topic: str, research: dict, style: Optional[dict] = None) -> ScriptOutput:
        ...

    @abstractmethod
    async def plan_scenes(self, script: str, duration: float = 60.0) -> list[ScenePlan]:
        ...

    @abstractmethod
    async def optimize_script(self, script: ScriptOutput, platform: str = "tiktok") -> ScriptOutput:
        ...

    @abstractmethod
    async def generate_hook(self, topic: str, style: str = "question") -> str:
        ...
