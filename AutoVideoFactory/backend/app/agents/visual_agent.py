from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger
from ..services.image_providers import ImageProviderRegistry

logger = get_logger("autovideofactory.agents.visual")


class VisualAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="visual", capabilities=[AgentCapability.VISUAL_CREATION])
        self._provider = ImageProviderRegistry.get("pollinations")

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        prompts = task.params.get("prompts", [])

        try:
            assets = []
            for i, p in enumerate(prompts):
                prompt_text = p.get("image_prompt", "") or p.get("prompt", "")
                try:
                    result = await self._provider.generate(prompt_text, width=1024, height=1024)
                    assets.append({
                        "scene": i,
                        "type": "image",
                        "file_path": result.get("url", ""),
                        "prompt": prompt_text,
                        "provider": "pollinations",
                    })
                except Exception:
                    assets.append({
                        "scene": i,
                        "type": "image",
                        "file_path": "",
                        "prompt": prompt_text,
                        "provider": "fallback",
                    })
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output={"assets": assets})
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
