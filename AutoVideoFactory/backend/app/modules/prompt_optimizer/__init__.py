from __future__ import annotations

from abc import abstractmethod
from typing import Any

from ..base import ModuleCapability, ModuleInterface
from ..prompt_generator import PromptOutput


class PromptOptimizerModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="prompt_optimization",
                description="Optimize prompts for better AI generation results",
                supported_providers=["llm", "template", "history"],
            ),
            ModuleCapability(
                name="a_b_testing",
                description="A/B test prompt variations to find best performers",
            ),
        ]

    @abstractmethod
    async def optimize(self, prompt: PromptOutput, target_provider: str) -> PromptOutput:
        ...

    @abstractmethod
    async def add_negative_prompt(self, prompt: str, undesirable: list[str]) -> str:
        ...

    @abstractmethod
    async def optimize_for_provider(self, prompt: str, provider: str) -> str:
        ...

    @abstractmethod
    async def generate_variations(self, prompt: PromptOutput, count: int = 3) -> list[PromptOutput]:
        ...
