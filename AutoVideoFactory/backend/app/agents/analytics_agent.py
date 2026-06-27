from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.analytics")


class AnalyticsAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="analytics", capabilities=[AgentCapability.ANALYTICS])

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        video_url = task.params.get("video_url", "")
        platform = task.params.get("platform", "tiktok")

        try:
            result = {
                "views": 15000,
                "likes": 2300,
                "comments": 145,
                "shares": 890,
                "avg_watch_percentage": 72.5,
                "platform": platform,
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
