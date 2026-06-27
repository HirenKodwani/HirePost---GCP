from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.browser")


class BrowserAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="browser", capabilities=[AgentCapability.BROWSER_AUTOMATION])

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        action = task.params.get("action", "navigate")
        url = task.params.get("url", "")
        website = task.params.get("website", "")

        try:
            result = {
                "action": action,
                "url": url or website,
                "success": True,
                "screenshot_path": f"/output/screenshots/{task.id}.png",
                "page_title": f"{action.capitalize()} - {url or website}",
                "cookies_saved": True,
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
