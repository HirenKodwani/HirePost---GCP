from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.publishing")


class PublishingAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="publishing", capabilities=[AgentCapability.PUBLISHING])

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        video_path = task.params.get("video_path", "")
        platform = task.params.get("platform", "tiktok")
        metadata = task.params.get("metadata", {})

        try:
            result = {
                "platform": platform,
                "video_url": f"https://{platform}.com/video/{task.id}",
                "published_at": __import__("datetime").datetime.now().__str__(),
                "success": True,
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
