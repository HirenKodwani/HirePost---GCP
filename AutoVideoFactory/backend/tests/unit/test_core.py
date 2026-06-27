from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.config import Environment, Settings
from app.core.events import Event, EventBus, EventType
from app.core.exceptions import (
    AutoVideoFactoryError,
    BrowserError,
    ConfigurationError,
    DatabaseError,
)
from app.core.logging import LoggerFactory


class TestSettings:
    def test_default_settings(self):
        s = Settings()
        assert s.app_name == "AutoVideoFactory"
        assert s.environment == Environment.DEVELOPMENT
        assert s.debug is True

    def test_custom_settings(self):
        s = Settings(app_name="Custom", debug=False)
        assert s.app_name == "Custom"
        assert s.debug is False

    def test_database_url_default(self):
        s = Settings()
        assert "sqlite" in s.database_url


class TestEventBus:
    @pytest.mark.asyncio
    async def test_publish_subscribe(self):
        bus = EventBus()
        received = []

        async def handler(event: Event):
            received.append(event)

        bus.subscribe(EventType.SYSTEM_STARTUP, handler)
        await bus.publish(Event(type=EventType.SYSTEM_STARTUP, source="test"))

        assert len(received) == 1
        assert received[0].type == EventType.SYSTEM_STARTUP

    @pytest.mark.asyncio
    async def test_wildcard_subscriber(self):
        bus = EventBus()
        received = []

        async def handler(event: Event):
            received.append(event)

        bus.subscribe_all(handler)
        await bus.publish(Event(type=EventType.JOB_CREATED, source="test"))
        await bus.publish(Event(type=EventType.AGENT_STARTED, source="test"))

        assert len(received) == 2

    @pytest.mark.asyncio
    async def test_event_history(self):
        bus = EventBus()
        await bus.publish(Event(type=EventType.SYSTEM_STARTUP, source="test"))
        await bus.publish(Event(type=EventType.JOB_CREATED, source="test"))

        history = bus.get_history()
        assert len(history) == 2

        filtered = bus.get_history(EventType.JOB_CREATED)
        assert len(filtered) == 1


class TestExceptions:
    def test_base_exception(self):
        err = AutoVideoFactoryError("test error", code="TEST")
        assert err.message == "test error"
        assert err.code == "TEST"

    def test_specific_exceptions(self):
        assert isinstance(ConfigurationError(), AutoVideoFactoryError)
        assert isinstance(DatabaseError(), AutoVideoFactoryError)
        assert isinstance(BrowserError(), AutoVideoFactoryError)

    def test_exception_details(self):
        err = AutoVideoFactoryError("error", details={"key": "value"})
        assert err.details["key"] == "value"
