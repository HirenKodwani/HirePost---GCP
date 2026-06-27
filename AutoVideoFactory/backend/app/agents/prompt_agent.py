from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger
from ..services.prompt_engineering import PromptEngineeringService

logger = get_logger("autovideofactory.agents.prompt")


class PromptAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="prompt", capabilities=[AgentCapability.PROMPT_ENGINEERING])
        self._prompt_engine = PromptEngineeringService()

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        scenes = task.params.get("scenes", [])

        try:
            prompts = []
            for i, scene in enumerate(scenes):
                desc = scene.get("description", "")
                image_prompt = await self._prompt_engine.generate_image_prompt(desc)
                video_prompt = await self._prompt_engine.generate_video_prompt(desc)
                prompts.append({
                    "scene": i,
                    "image_prompt": image_prompt,
                    "video_prompt": video_prompt,
                })
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output={"prompts": prompts})
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
