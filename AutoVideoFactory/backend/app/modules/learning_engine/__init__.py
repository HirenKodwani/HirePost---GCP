from __future__ import annotations

from abc import abstractmethod
from typing import Any

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class LearningRecord(BaseModel):
    input_data: dict = {}
    output_data: dict = {}
    feedback: float = 0.0
    source: str = ""


class LearningEngineModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="feedback_learning",
                description="Learn from content performance and user feedback",
                supported_providers=["local", "fine_tuning"],
            ),
            ModuleCapability(
                name="prompt_evolution",
                description="Evolve prompts based on historical performance",
            ),
        ]

    @abstractmethod
    async def record(self, data: LearningRecord) -> None:
        ...

    @abstractmethod
    async def get_insights(self, data_type: str) -> list[dict]:
        ...

    @abstractmethod
    async def improve_prompts(self, prompt_type: str) -> list[dict]:
        ...

    @abstractmethod
    async def suggest_improvements(self, video_id: str) -> dict:
        ...
