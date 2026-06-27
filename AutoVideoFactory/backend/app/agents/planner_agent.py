from __future__ import annotations

from typing import Any, Optional

from .base import (
    AgentCapability,
    AgentMessage,
    AgentResult,
    AgentStatus,
    AgentTask,
    BaseAgent,
)
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.planner")


class PlannerAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="planner",
            capabilities=[AgentCapability.PLANNING],
        )

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        logger.info("Planning task", extra={"task_type": task.task_type, "params": task.params})

        try:
            plan = await self._create_plan(task)
            self._status = AgentStatus.COMPLETED
            return AgentResult(
                task_id=task.id,
                success=True,
                output={"plan": plan, "steps": plan.get("steps", [])},
            )
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(
                task_id=task.id, success=False, error=str(e)
            )

    async def _create_plan(self, task: AgentTask) -> dict[str, Any]:
        pipeline_type = task.params.get("pipeline_type", "full")
        steps = []

        if pipeline_type == "full":
            steps = [
                {"agent": "trend", "action": "discover_trends", "params": {}},
                {"agent": "research", "action": "research_topic", "params": {}},
                {"agent": "script", "action": "write_script", "params": {}},
                {"agent": "prompt", "action": "generate_prompts", "params": {}},
                {"agent": "voice", "action": "generate_voice", "params": {}},
                {"agent": "visual", "action": "generate_visuals", "params": {}},
                {"agent": "video", "action": "generate_video", "params": {}},
                {"agent": "editing", "action": "edit_video", "params": {}},
                {"agent": "subtitle", "action": "add_subtitles", "params": {}},
                {"agent": "qa", "action": "review", "params": {}},
                {"agent": "publishing", "action": "publish", "params": {}},
            ]
        elif pipeline_type == "research_only":
            steps = [
                {"agent": "trend", "action": "discover_trends", "params": {}},
                {"agent": "research", "action": "research_topic", "params": {}},
            ]
        elif pipeline_type == "script_only":
            steps = [
                {"agent": "research", "action": "research_topic", "params": {}},
                {"agent": "script", "action": "write_script", "params": {}},
            ]

        return {
            "pipeline_type": pipeline_type,
            "steps": steps,
            "estimated_duration_ms": len(steps) * 60000,
            "parallel_steps": [],
        }
