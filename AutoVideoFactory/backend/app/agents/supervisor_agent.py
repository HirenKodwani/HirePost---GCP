from __future__ import annotations

from typing import Any, Optional

from .base import AgentCapability, AgentMessage, AgentResult, AgentStatus, AgentTask, BaseAgent
from .orchestrator import AgentOrchestrator
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.supervisor")


class SupervisorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="supervisor",
            capabilities=[AgentCapability.SUPERVISION],
        )
        self._orchestrator = AgentOrchestrator()

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        command = task.params.get("command", "status")

        try:
            if command == "status":
                result = {"agents": self._orchestrator.get_all_agent_statuses(), "pipelines": len(self._orchestrator.get_all_pipelines())}
            elif command == "start_pipeline":
                pipeline_id = await self._orchestrator.run_pipeline(
                    name=task.params.get("pipeline_name", "auto"),
                    steps=task.params.get("steps", []),
                    params=task.params.get("params"),
                )
                result = {"pipeline_id": pipeline_id, "status": "started"}
            elif command == "cancel_pipeline":
                success = await self._orchestrator.cancel_pipeline(task.params.get("pipeline_id", ""))
                result = {"cancelled": success}
            elif command == "health_check":
                result = self._perform_health_check()
            else:
                result = {"error": f"Unknown command: {command}"}

            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))

    def _perform_health_check(self) -> dict[str, Any]:
        agents = self._orchestrator.get_all_agent_statuses()
        return {
            "healthy": all(a["status"] != "failed" for a in agents),
            "total_agents": len(agents),
            "active_agents": sum(1 for a in agents if a["status"] == "running"),
            "idle_agents": sum(1 for a in agents if a["status"] == "idle"),
        }
