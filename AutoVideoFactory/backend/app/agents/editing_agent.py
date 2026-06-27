from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger

logger = get_logger("autovideofactory.agents.editing")


class EditingAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="editing", capabilities=[AgentCapability.VIDEO_EDITING])

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        video_path = task.params.get("video_path", "")
        voice_path = task.params.get("voice_path")
        music_path = task.params.get("music_path")

        try:
            result = {
                "input_video": video_path,
                "voiceover": voice_path,
                "background_music": music_path,
                "output_path": video_path.replace(".mp4", "_final.mp4") if video_path else "",
                "effects_applied": ["voiceover", "background_music"],
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
