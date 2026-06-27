from __future__ import annotations

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger
from ..services.voice_service import VoiceService

logger = get_logger("autovideofactory.agents.voice")


class VoiceAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="voice", capabilities=[AgentCapability.VOICE_GENERATION])
        self._voice = VoiceService()

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        script = task.params.get("script", "")
        voice_id = task.params.get("voice_id", "en-US-JennyNeural")

        try:
            result = await self._voice.generate_edge_tts(script[:500], voice=voice_id)
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
