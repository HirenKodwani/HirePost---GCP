from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import BrowserProviderInterface, ModuleCapability, ModuleInterface, ModuleStatus


class BrowserActionResult(BaseModel):
    success: bool
    data: Optional[Any] = None
    screenshot: Optional[bytes] = None
    error: Optional[str] = None


class BrowserAutomationModuleInterface(ModuleInterface[Any]):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="browser_navigation",
                description="Navigate websites and interact with pages",
                supported_providers=["playwright", "selenium"],
            ),
            ModuleCapability(
                name="session_management",
                description="Save, restore, and manage browser sessions",
                supported_providers=["local", "database"],
            ),
            ModuleCapability(
                name="vision_automation",
                description="Use screenshots and vision to interact with pages",
                supported_providers=["ocr", "openai_vision"],
            ),
        ]

    @abstractmethod
    async def launch(self, headless: bool = False) -> bool:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def navigate(self, url: str, timeout: Optional[int] = None) -> BrowserActionResult:
        ...

    @abstractmethod
    async def click(self, selector: str, timeout: Optional[int] = None) -> BrowserActionResult:
        ...

    @abstractmethod
    async def type_text(self, selector: str, text: str, delay: int = 50) -> BrowserActionResult:
        ...

    @abstractmethod
    async def screenshot(self, full_page: bool = False) -> bytes:
        ...

    @abstractmethod
    async def get_html(self, selector: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def execute_script(self, script: str) -> Any:
        ...

    @abstractmethod
    async def wait_for_selector(self, selector: str, timeout: int = 30000) -> bool:
        ...

    @abstractmethod
    async def wait_for_navigation(self, timeout: int = 60000) -> bool:
        ...

    @abstractmethod
    async def upload_file(self, selector: str, file_path: str) -> BrowserActionResult:
        ...

    @abstractmethod
    async def scroll(self, direction: str = "down", amount: int = 300) -> None:
        ...

    @abstractmethod
    async def extract_text(self, selector: str) -> str:
        ...

    @abstractmethod
    async def extract_links(self, selector: str = "a") -> list[dict[str, str]]:
        ...
