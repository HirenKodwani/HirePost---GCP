from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from .base import AgentMessage, AgentResult, AgentStatus, AgentTask, BaseAgent
from ..core.events import Event, EventBus, EventType
from ..core.logging import get_logger

logger = get_logger("autovideofactory.orchestrator")


class PipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Pipeline:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    name: str = ""
    steps: list[dict] = field(default_factory=list)
    status: PipelineStatus = PipelineStatus.PENDING
    current_step: int = 0
    results: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class AgentOrchestrator:
    _instance: Optional[AgentOrchestrator] = None
    _agents: dict[str, BaseAgent] = {}
    _pipelines: dict[str, Pipeline] = {}
    _event_bus: EventBus = None

    def __new__(cls) -> AgentOrchestrator:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._agents = {}
            cls._instance._pipelines = {}
            cls._instance._event_bus = EventBus()
        return cls._instance

    def register_agent(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent
        logger.info("Agent registered", extra={"agent": agent.name, "capabilities": [c.value for c in agent.capabilities]})

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        return self._agents.get(name)

    def get_agents_by_capability(self, capability: str) -> list[BaseAgent]:
        from .base import AgentCapability
        cap = AgentCapability(capability)
        return [a for a in self._agents.values() if cap in a.capabilities]

    async def run_pipeline(self, name: str, steps: list[dict], params: Optional[dict] = None) -> str:
        pipeline = Pipeline(name=name, steps=steps, status=PipelineStatus.RUNNING, started_at=datetime.now(timezone.utc))
        self._pipelines[pipeline.id] = pipeline

        await self._event_bus.publish(Event(type=EventType.PIPELINE_STARTED, source="orchestrator", data={"pipeline_id": pipeline.id, "name": name}))

        for i, step in enumerate(steps):
            if pipeline.status == PipelineStatus.CANCELLED:
                break

            pipeline.current_step = i
            agent_name = step.get("agent")
            action = step.get("action")
            step_params = step.get("params", {})

            agent = self.get_agent(agent_name)
            if not agent:
                error = f"Agent not found: {agent_name}"
                pipeline.errors.append(error)
                pipeline.status = PipelineStatus.FAILED
                break

            task = AgentTask(
                task_type=action,
                params={**step_params, **(params or {}), **pipeline.results},
                priority=step.get("priority", 0),
            )

            try:
                result = await agent.execute(task)
                pipeline.results[f"{agent_name}_{action}"] = result.output

                await self._event_bus.publish(
                    Event(
                        type=EventType.PIPELINE_STEP_COMPLETED,
                        source="orchestrator",
                        data={"pipeline_id": pipeline.id, "step": i, "agent": agent_name, "action": action, "success": result.success},
                    )
                )

                if not result.success:
                    pipeline.errors.append(f"Step {i} ({agent_name}/{action}): {result.error}")
                    pipeline.status = PipelineStatus.FAILED
                    break

            except Exception as e:
                pipeline.errors.append(f"Step {i} ({agent_name}/{action}): {str(e)}")
                pipeline.status = PipelineStatus.FAILED
                break

        if pipeline.status == PipelineStatus.RUNNING:
            pipeline.status = PipelineStatus.COMPLETED

        pipeline.completed_at = datetime.now(timezone.utc)
        event_type = EventType.PIPELINE_COMPLETED if pipeline.status == PipelineStatus.COMPLETED else EventType.PIPELINE_FAILED

        await self._event_bus.publish(
            Event(
                type=event_type,
                source="orchestrator",
                data={
                    "pipeline_id": pipeline.id,
                    "name": name,
                    "status": pipeline.status.value,
                    "steps_completed": pipeline.current_step,
                    "errors": pipeline.errors,
                },
            )
        )

        return pipeline.id

    async def cancel_pipeline(self, pipeline_id: str) -> bool:
        pipeline = self._pipelines.get(pipeline_id)
        if pipeline and pipeline.status == PipelineStatus.RUNNING:
            pipeline.status = PipelineStatus.CANCELLED
            for agent in self._agents.values():
                if agent.status == AgentStatus.RUNNING:
                    await agent.cancel()
            return True
        return False

    def get_pipeline(self, pipeline_id: str) -> Optional[Pipeline]:
        return self._pipelines.get(pipeline_id)

    def get_all_pipelines(self) -> list[Pipeline]:
        return list(self._pipelines.values())

    def get_all_agent_statuses(self) -> list[dict]:
        return [a.get_status_info() for a in self._agents.values()]

    async def send_message_between_agents(self, sender: str, receiver: str, message_type: str, content: dict[str, Any], correlation_id: Optional[str] = None) -> Optional[AgentMessage]:
        sender_agent = self.get_agent(sender)
        receiver_agent = self.get_agent(receiver)
        if sender_agent and receiver_agent:
            return await sender_agent.send_message(receiver_agent, message_type, content, correlation_id)
        return None
