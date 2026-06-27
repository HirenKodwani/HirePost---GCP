from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from ...core.config import settings
from ...core.exceptions import BrowserSessionError
from ...core.logging import get_logger
from ..base import ModuleHealth, ModuleStatus
from . import BrowserSessionModuleInterface, SessionInfo

logger = get_logger("autovideofactory.browser.session")


class LocalSessionManager(BrowserSessionModuleInterface):
    _sessions: dict[str, dict[str, Any]] = {}
    _active_session_id: Optional[str] = None

    def __init__(self) -> None:
        self._status = ModuleStatus.UNINITIALIZED
        self._sessions_dir = settings.sessions_dir
        self._sessions_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self, config: Optional[dict] = None) -> None:
        self._status = ModuleStatus.READY
        await self._load_sessions()
        logger.info("Session manager initialized", extra={"sessions_dir": str(self._sessions_dir)})

    async def shutdown(self) -> None:
        await self._save_all_sessions()
        self._sessions.clear()
        self._status = ModuleStatus.UNINITIALIZED

    async def health_check(self) -> ModuleHealth:
        return ModuleHealth(
            status=self._status,
            message=f"Session manager ready, {len(self._sessions)} sessions",
        )

    def get_capabilities(self):
        return [
            ModuleCapability(
                name="session_persistence",
                description="Save and restore browser sessions with cookies and local storage",
                supported_providers=["local"],
            ),
            ModuleCapability(
                name="session_management",
                description="Full lifecycle management of browser sessions",
                supported_providers=["local"],
            ),
        ]

    async def create_session(self, profile_name: str, **kwargs: Any) -> SessionInfo:
        session_id = kwargs.get("session_id", os.urandom(16).hex())
        now = datetime.now(timezone.utc)
        session = {
            "session_id": session_id,
            "profile_name": profile_name,
            "browser_type": kwargs.get("browser_type", "chromium"),
            "is_active": True,
            "created_at": now.isoformat(),
            "last_used_at": now.isoformat(),
            "expires_at": (now + timedelta(minutes=settings.browser_session_ttl_minutes)).isoformat(),
            "page_url": kwargs.get("page_url", ""),
            "cookies": [],
            "storage_state": {},
            "viewport_width": kwargs.get("viewport_width", settings.browser_viewport_width),
            "viewport_height": kwargs.get("viewport_height", settings.browser_viewport_height),
            "user_agent": kwargs.get("user_agent", ""),
        }
        self._sessions[session_id] = session
        self._active_session_id = session_id
        await self._save_session(session_id)
        logger.info("Session created", extra={"session_id": session_id, "profile": profile_name})
        return SessionInfo(**session)

    async def restore_session(self, session_id: str) -> bool:
        session = self._sessions.get(session_id)
        if not session:
            raise BrowserSessionError(f"Session not found: {session_id}")
        session["is_active"] = True
        session["last_used_at"] = datetime.now(timezone.utc).isoformat()
        self._active_session_id = session_id
        return True

    async def save_session(self, session_id: str) -> None:
        await self._save_session(session_id)

    async def close_session(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session:
            session["is_active"] = False
            await self._save_session(session_id)
        if self._active_session_id == session_id:
            self._active_session_id = None

    async def list_sessions(self) -> list[SessionInfo]:
        return [SessionInfo(**s) for s in self._sessions.values()]

    async def get_active_session(self) -> Optional[SessionInfo]:
        if self._active_session_id and self._active_session_id in self._sessions:
            return SessionInfo(**self._sessions[self._active_session_id])
        return None

    async def export_cookies(self, session_id: str) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if not session:
            raise BrowserSessionError(f"Session not found: {session_id}")
        return {"cookies": session.get("cookies", []), "storage_state": session.get("storage_state", {})}

    async def import_cookies(self, session_id: str, cookies: dict[str, Any]) -> None:
        session = self._sessions.get(session_id)
        if not session:
            raise BrowserSessionError(f"Session not found: {session_id}")
        session["cookies"] = cookies.get("cookies", [])
        session["storage_state"] = cookies.get("storage_state", {})

    async def _load_sessions(self) -> None:
        if not self._sessions_dir.exists():
            return
        for f in self._sessions_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                self._sessions[data["session_id"]] = data
            except Exception as e:
                logger.warning(f"Failed to load session {f.name}: {e}")

    async def _save_session(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session:
            path = self._sessions_dir / f"{session_id}.json"
            path.write_text(json.dumps(session, indent=2, default=str))

    async def _save_all_sessions(self) -> None:
        for session_id in list(self._sessions.keys()):
            await self._save_session(session_id)
