from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger
from ..services.llm_client import get_llm_client

logger = get_logger("autovideofactory.agents.research")


class ResearchAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="research", capabilities=[AgentCapability.RESEARCH])
        self._llm = get_llm_client()

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        topic = task.params.get("topic", "unknown")
        logger.info("Researching topic", extra={"topic": topic})

        try:
            research = await self._llm.generate_json(
                f"Research the topic '{topic}' for a short-form video. "
                f"Provide a summary, 5 key points, and 3 potential sources.",
                system_prompt="Return JSON with 'summary', 'key_points' (array of strings), and 'sources' (array of strings).",
            )
            research_data = {
                "topic": topic,
                "summary": research.get("summary", f"Research summary for {topic}"),
                "key_points": research.get("key_points", [f"Key point 1 about {topic}", f"Key point 2 about {topic}"]),
                "sources": research.get("sources", []),
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=research_data)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
