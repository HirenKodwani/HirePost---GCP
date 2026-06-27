from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger
from ..services.llm_client import get_llm_client

logger = get_logger("autovideofactory.agents.trend")


class TrendAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="trend", capabilities=[AgentCapability.TREND_ANALYSIS])
        self._llm = get_llm_client()

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        platform = task.params.get("platform", "tiktok")
        niche = task.params.get("niche", "general")

        try:
            trends_data = await self._llm.generate_json(
                f"List 5 trending topics in '{niche}' for {platform} short-form videos. "
                f"Include a relevance score for each.",
                system_prompt="Return JSON with 'trends' array containing objects with 'title', 'score' (0-100), and 'reason'.",
            )
            trends = {
                "trends": trends_data.get("trends", [
                    {"title": f"Trending in {niche} #1", "score": 95, "platform": platform},
                    {"title": f"Trending in {niche} #2", "score": 88, "platform": platform},
                ]),
                "platform": platform,
                "niche": niche,
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=trends)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
