from __future__ import annotations

import os
from pathlib import Path

from .base import AgentCapability, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.logging import get_logger
from ..services.video_editor import VideoEditorService

logger = get_logger("autovideofactory.agents.video")


class VideoAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="video", capabilities=[AgentCapability.VIDEO_PRODUCTION])
        self._editor = VideoEditorService()

    async def execute(self, task: AgentTask) -> AgentResult:
        self._status = AgentStatus.RUNNING
        self._current_task = task
        assets = task.params.get("assets", [])

        try:
            clips = []
            assets_dir = Path("output/assets")
            assets_dir.mkdir(parents=True, exist_ok=True)
            for i, a in enumerate(assets):
                path = a.get("file_path", "")
                if path and os.path.exists(path):
                    clips.append({"file_path": path, "duration": 5})
                else:
                    placeholder = await self._editor._create_placeholder(1080, 1920, 5)
                    clips.append({"file_path": placeholder, "duration": 5})

            voiceover_path = task.params.get("voiceover_path", "")
            video_path = await self._editor.compose(
                clips=clips,
                voiceover_path=voiceover_path if voiceover_path and Path(voiceover_path).exists() else None,
            )

            result = {
                "video_path": video_path,
                "clips": [{"asset": a, "start": i * 5, "end": (i + 1) * 5} for i, a in enumerate(assets)],
                "duration": len(assets) * 5,
            }
            self._status = AgentStatus.COMPLETED
            return AgentResult(task_id=task.id, success=True, output=result)
        except Exception as e:
            self._status = AgentStatus.FAILED
            return AgentResult(task_id=task.id, success=False, error=str(e))
