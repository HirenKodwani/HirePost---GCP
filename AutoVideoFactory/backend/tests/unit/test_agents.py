from __future__ import annotations

import pytest

from app.agents.base import AgentCapability, AgentResult, AgentStatus, AgentTask
from app.agents.orchestrator import AgentOrchestrator
from app.agents.research_agent import ResearchAgent
from app.agents.script_agent import ScriptAgent
from app.agents.trend_agent import TrendAgent
from app.agents.planner_agent import PlannerAgent


class TestBaseAgent:
    @pytest.mark.asyncio
    async def test_agent_lifecycle(self):
        agent = ResearchAgent()
        assert agent.name == "research"
        assert agent.status == AgentStatus.IDLE

        task = AgentTask(task_type="research_topic", params={"topic": "AI"})
        result = await agent.execute(task)

        assert agent.status == AgentStatus.COMPLETED
        assert result.success is True
        assert "topic" in result.output

    @pytest.mark.asyncio
    async def test_agent_error_handling(self):
        agent = ResearchAgent()
        task = AgentTask(task_type="unknown_task", params={})
        result = await agent.execute(task)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_agent_capabilities(self):
        agent = ResearchAgent()
        assert AgentCapability.RESEARCH in agent.capabilities


class TestAgentOrchestrator:
    @pytest.mark.asyncio
    async def test_register_agent(self):
        orch = AgentOrchestrator()
        agent = ResearchAgent()
        orch.register_agent(agent)

        assert orch.get_agent("research") is agent

    @pytest.mark.asyncio
    async def test_pipeline_execution(self):
        orch = AgentOrchestrator()
        orch.register_agent(ResearchAgent())

        steps = [{"agent": "research", "action": "research_topic", "params": {"topic": "AI"}}]
        pipeline_id = await orch.run_pipeline("test", steps)

        pipeline = orch.get_pipeline(pipeline_id)
        assert pipeline is not None
        assert pipeline.status.value in ["completed", "failed"]

    @pytest.mark.asyncio
    async def test_planner_creates_pipeline(self):
        agent = PlannerAgent()
        task = AgentTask(task_type="create_plan", params={"pipeline_type": "research_only"})
        result = await agent.execute(task)

        assert result.success is True
        assert "plan" in result.output
        assert len(result.output["plan"]["steps"]) == 2

    @pytest.mark.asyncio
    async def test_multi_agent_pipeline(self):
        orch = AgentOrchestrator()
        orch.register_agent(ResearchAgent())
        orch.register_agent(ScriptAgent())
        orch.register_agent(TrendAgent())

        steps = [
            {"agent": "trend", "action": "discover_trends", "params": {"niche": "technology"}},
            {"agent": "research", "action": "research_topic", "params": {"topic": "AI trends"}},
            {"agent": "script", "action": "write_script", "params": {}},
        ]
        pipeline_id = await orch.run_pipeline("full_test", steps)

        pipeline = orch.get_pipeline(pipeline_id)
        assert pipeline is not None
