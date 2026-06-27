from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.subtitle")


class SubtitleAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="subtitle", capabilities=[AgentCapability.SUBTITLE_GENERATION])

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        voice_segments = task.params.get("voice_segments", [])
        script = task.params.get("script", "")

        try:
            result = {
                "subtitle_path": f"/output/subtitles/{task.id}.srt",
                "segments": [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in voice_segments],
                "format": "srt",
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
