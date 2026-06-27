from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel


class ModuleStatus(str, Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class ModuleHealth:
    status: ModuleStatus = ModuleStatus.UNINITIALIZED
    last_check: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)


class ModuleCapability(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    supported_providers: list[str] = field(default_factory=list)
    config_schema: dict[str, Any] = field(default_factory=dict)


T = TypeVar("T")


class ModuleInterface(ABC, Generic[T]):
    _status: ModuleStatus = ModuleStatus.UNINITIALIZED
    _health: ModuleHealth = field(default_factory=ModuleHealth)
    _capabilities: list[ModuleCapability] = field(default_factory=list)
    _config: Optional[T] = None

    @abstractmethod
    async def initialize(self, config: Optional[T] = None) -> None:
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        ...

    @abstractmethod
    async def health_check(self) -> ModuleHealth:
        ...

    @abstractmethod
    def get_capabilities(self) -> list[ModuleCapability]:
        ...

    @property
    def status(self) -> ModuleStatus:
        return self._status

    @property
    def is_ready(self) -> bool:
        return self._status == ModuleStatus.READY


class ProviderInterface(ABC, Generic[T]):
    _provider_name: str = ""
    _is_connected: bool = False

    @abstractmethod
    async def connect(self) -> bool:
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        ...

    @property
    def provider_name(self) -> str:
        return self._provider_name


class ConfigProviderInterface(ProviderInterface[T]):
    @abstractmethod
    async def get_config(self) -> T:
        ...

    @abstractmethod
    async def set_config(self, config: T) -> None:
        ...

    @abstractmethod
    async def validate_config(self, config: T) -> bool:
        ...


class BrowserProviderInterface(ProviderInterface[T]):
    @abstractmethod
    async def navigate(self, url: str, **kwargs: Any) -> Any:
        ...

    @abstractmethod
    async def screenshot(self, **kwargs: Any) -> bytes:
        ...

    @abstractmethod
    async def click(self, selector: str, **kwargs: Any) -> bool:
        ...

    @abstractmethod
    async def type_text(self, selector: str, text: str, **kwargs: Any) -> bool:
        ...

    @abstractmethod
    async def get_text(self, selector: str, **kwargs: Any) -> str:
        ...

    @abstractmethod
    async def upload_file(self, selector: str, file_path: str, **kwargs: Any) -> bool:
        ...

    @abstractmethod
    async def wait_for_selector(self, selector: str, **kwargs: Any) -> bool:
        ...

    @abstractmethod
    async def evaluate(self, script: str, **kwargs: Any) -> Any:
        ...


class ContentGenerationProviderInterface(ProviderInterface[T]):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> Any:
        ...

    @abstractmethod
    async def get_status(self, task_id: str) -> str:
        ...

    @abstractmethod
    async def get_result(self, task_id: str) -> Any:
        ...


class AgentInterface(ABC, Generic[T]):
    _agent_name: str = ""
    _is_running: bool = False

    @abstractmethod
    async def execute(self, task: T) -> Any:
        ...

    @abstractmethod
    async def cancel(self) -> None:
        ...

    @abstractmethod
    async def get_status(self) -> dict[str, Any]:
        ...

    @property
    def agent_name(self) -> str:
        return self._agent_name
