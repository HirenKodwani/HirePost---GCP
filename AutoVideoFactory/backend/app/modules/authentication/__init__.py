from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleInterface, ModuleStatus


class UserSession(BaseModel):
    user_id: str
    username: str
    roles: list[str] = ["user"]
    token: str = ""
    expires_at: Optional[str] = None


class AuthenticationModuleInterface(ModuleInterface[Any]):
    def get_capabilities(self):
        from ..base import ModuleCapability
        return [
            ModuleCapability(
                name="authentication",
                description="User authentication and authorization",
                supported_providers=["jwt", "oauth", "api_key"],
            )
        ]

    @abstractmethod
    async def authenticate(self, username: str, password: str) -> Optional[UserSession]:
        ...

    @abstractmethod
    async def verify_token(self, token: str) -> Optional[UserSession]:
        ...

    @abstractmethod
    async def create_user(self, username: str, password: str, roles: Optional[list[str]] = None) -> str:
        ...

    @abstractmethod
    async def check_permission(self, user_id: str, permission: str) -> bool:
        ...
