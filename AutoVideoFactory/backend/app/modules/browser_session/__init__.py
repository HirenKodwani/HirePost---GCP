from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class SessionInfo(BaseModel):
    session_id: str
    profile_name: str
    browser_type: str = "chromium"
    is_active: bool = False
    created_at: Optional[str] = None
    last_used_at: Optional[str] = None
    expires_at: Optional[str] = None
    page_url: Optional[str] = None


class BrowserSessionModuleInterface(ModuleInterface[Any]):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="session_persistence",
                description="Save and restore browser sessions with cookies and local storage",
            ),
            SessionManagementCapability(),
        ]

    @abstractmethod
    async def create_session(self, profile_name: str, **kwargs: Any) -> SessionInfo:
        ...

    @abstractmethod
    async def restore_session(self, session_id: str) -> bool:
        ...

    @abstractmethod
    async def save_session(self, session_id: str) -> None:
        ...

    @abstractmethod
    async def close_session(self, session_id: str) -> None:
        ...

    @abstractmethod
    async def list_sessions(self) -> list[SessionInfo]:
        ...

    @abstractmethod
    async def get_active_session(self) -> Optional[SessionInfo]:
        ...

    @abstractmethod
    async def export_cookies(self, session_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    async def import_cookies(self, session_id: str, cookies: dict[str, Any]) -> None:
        ...


class SessionManagementCapability(ModuleCapability):
    def __init__(self):
        super().__init__(
            name="session_management",
            description="Full lifecycle management of browser sessions",
            supported_providers=["local", "database", "redis"],
        )
