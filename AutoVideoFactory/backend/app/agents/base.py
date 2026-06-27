from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentCapability(str, Enum):
    RESEARCH = "research"
    SCRIPT_WRITING = "script_writing"
    TREND_ANALYSIS = "trend_analysis"
    PROMPT_ENGINEERING = "prompt_engineering"
    VOICE_GENERATION = "voice_generation"
    VISUAL_CREATION = "visual_creation"
    VIDEO_PRODUCTION = "video_production"
    VIDEO_EDITING = "video_editing"
    SUBTITLE_GENERATION = "subtitle_generation"
    PUBLISHING = "publishing"
    ANALYTICS = "analytics"
    LEARNING = "learning"
    QUALITY_ASSURANCE = "quality_assurance"
    RECOVERY = "recovery"
    BROWSER_AUTOMATION = "browser_automation"
    PLANNING = "planning"
    SUPERVISION = "supervision"


@dataclass
class AgentMessage:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    sender: str = ""
    receiver: str = ""
    message_type: str = "task"
    content: dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    priority: int = 0


@dataclass
class AgentTask:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    task_type: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    deadline: Optional[datetime] = None
    dependencies: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AgentResult:
    task_id: str = ""
    success: bool = False
    output: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: float = 0.0
    metrics: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    _name: str = ""
    _status: AgentStatus = AgentStatus.IDLE
    _capabilities: list[AgentCapability] = []
    _current_task: Optional[AgentTask] = None
    _message_queue: list[AgentMessage] = []

    def __init__(self, name: str, capabilities: Optional[list[AgentCapability]] = None) -> None:
        self._name = name
        self._capabilities = capabilities or []
        self._message_queue = []
        self._current_task = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> AgentStatus:
        return self._status

    @property
    def capabilities(self) -> list[AgentCapability]:
        return self._capabilities.copy()

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        ...

    async def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        self._message_queue.append(message)
        return None

    async def send_message(self, receiver: BaseAgent, message_type: str, content: dict[str, Any], correlation_id: Optional[str] = None) -> AgentMessage:
        msg = AgentMessage(
            sender=self._name,
            receiver=receiver.name,
            message_type=message_type,
            content=content,
            correlation_id=correlation_id,
        )
        return await receiver.receive_message(msg)

    async def cancel(self) -> None:
        self._status = AgentStatus.CANCELLED
        self._current_task = None

    def get_status_info(self) -> dict[str, Any]:
        return {
            "name": self._name,
            "status": self._status.value,
            "capabilities": [c.value for c in self._capabilities],
            "current_task": self._current_task.id if self._current_task else None,
            "queue_size": len(self._message_queue),
        }
