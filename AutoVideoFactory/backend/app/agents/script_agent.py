from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger
from ..services.prompt_engineering import PromptEngineeringService

logger = get_logger("autovideofactory.agents.script")


class ScriptAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="script", capabilities=[AgentCapability.SCRIPT_WRITING])
        self._prompt_engine = PromptEngineeringService()

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        topic = task.params.get("topic", "unknown")
        research = task.params.get("research", {})
        duration = task.params.get("duration", 60)

        try:
            content = await self._prompt_engine.generate_script(topic, research, duration)
            title = await self._prompt_engine.generate_title(topic)
            word_count = len(content.split())
            scenes = []
            for i, paragraph in enumerate(content.split("\n\n")):
                if paragraph.strip():
                    scenes.append({
                        "scene_number": i + 1,
                        "description": paragraph.strip()[:100],
                        "duration": max(5, int(duration / max(len(content.split("\n\n")), 1))),
                    })
            script = {
                "title": title or f"Video about {topic}",
                "content": content,
                "scenes": scenes if scenes else [
                    {"scene_number": 1, "description": f"Hook about {topic}", "duration": 10},
                    {"scene_number": 2, "description": f"Main content about {topic}", "duration": 30},
                    {"scene_number": 3, "description": "Call to action", "duration": 10},
                ],
                "word_count": word_count,
                "estimated_duration": duration,
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=script)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
