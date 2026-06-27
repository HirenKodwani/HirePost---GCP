from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Coroutine, Optional

from .logging import get_logger

logger = get_logger("autovideofactory.events")


class EventPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventType(str, Enum):
    # System events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"

    # Job events
    JOB_CREATED = "job.created"
    JOB_STARTED = "job.started"
    JOB_PROGRESS = "job.progress"
    JOB_COMPLETED = "job.completed"
    JOB_FAILED = "job.failed"
    JOB_CANCELLED = "job.cancelled"

    # Agent events
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"
    AGENT_MESSAGE = "agent.message"

    # Browser events
    BROWSER_LAUNCHED = "browser.launched"
    BROWSER_NAVIGATED = " browser.navigated"
    BROWSER_ERROR = "browser.error"
    BROWSER_SESSION_CREATED = "browser.session.created"
    BROWSER_SESSION_CLOSED = "browser.session.closed"

    # Content events
    CONTENT_GENERATED = "content.generated"
    CONTENT_FAILED = "content.failed"
    VIDEO_RENDERED = "video.rendered"
    VIDEO_PUBLISHED = "video.published"

    # Analytics events
    ANALYTICS_COLLECTED = "analytics.collected"
    METRIC_UPDATED = "metric.updated"

    # Pipeline events
    PIPELINE_STARTED = "pipeline.started"
    PIPELINE_STEP_COMPLETED = "pipeline.step.completed"
    PIPELINE_COMPLETED = "pipeline.completed"
    PIPELINE_FAILED = "pipeline.failed"

    # User events
    USER_ACTION = "user.action"


@dataclass
class Event:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    type: EventType = EventType.SYSTEM_STARTUP
    source: str = "system"
    data: dict[str, Any] = field(default_factory=dict)
    priority: EventPriority = EventPriority.NORMAL
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None


EventHandler = Callable[[Event], Coroutine[Any, Any, None]]


class EventBus:
    _instance: Optional[EventBus] = None
    _subscribers: dict[EventType, list[EventHandler]] = {}
    _wildcard_subscribers: list[EventHandler] = []
    _history: list[Event] = []
    _max_history: int = 1000
    _lock = asyncio.Lock()

    def __new__(cls) -> EventBus:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers = {}
            cls._instance._wildcard_subscribers = []
            cls._instance._history = []
        return cls._instance

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.debug("Subscribed to event", extra={"event_type": event_type.value})

    def subscribe_all(self, handler: EventHandler) -> None:
        self._wildcard_subscribers.append(handler)

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                h for h in self._subscribers[event_type] if h is not handler
            ]

    async def publish(self, event: Event) -> None:
        async with self._lock:
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history.pop(0)

        tasks = []
        for handler in self._wildcard_subscribers:
            tasks.append(self._safe_dispatch(handler, event))

        if event.type in self._subscribers:
            for handler in self._subscribers[event.type]:
                tasks.append(self._safe_dispatch(handler, event))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_dispatch(self, handler: EventHandler, event: Event) -> None:
        try:
            await handler(event)
        except Exception as e:
            logger.error(
                "Event handler failed",
                extra={
                    "event_type": event.type.value,
                    "handler": handler.__name__,
                    "error": str(e),
                },
            )

    def get_history(
        self,
        event_type: Optional[EventType] = None,
        limit: int = 100,
    ) -> list[Event]:
        if event_type:
            filtered = [e for e in self._history if e.type == event_type]
        else:
            filtered = list(self._history)
        return filtered[-limit:]

    def clear_history(self) -> None:
        self._history.clear()


event_bus = EventBus()
