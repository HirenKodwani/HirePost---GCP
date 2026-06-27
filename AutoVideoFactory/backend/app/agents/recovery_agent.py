from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.recovery")


class RecoveryAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="recovery", capabilities=[AgentCapability.RECOVERY])

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        failed_step = task.params.get("failed_step", {})
        error = task.params.get("error", "unknown")

        try:
            recovery_plan = {
                "retry_strategy": "exponential_backoff",
                "max_retries": 3,
                "fallback_action": "skip_step" if "critical" not in error else "abort_pipeline",
                "recovery_actions": [
                    "Clear browser cache and retry",
                    "Switch to backup provider",
                    "Reduce generation quality",
                ],
                "estimated_recovery_time_ms": 30000,
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=recovery_plan)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
