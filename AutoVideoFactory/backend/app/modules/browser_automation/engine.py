from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    async_playwright,
)

from ...core.config import settings
from ...core.exceptions import BrowserError, BrowserSessionError
from ...core.logging import get_logger
from ..base import ModuleHealth, ModuleStatus
from . import BrowserActionResult, BrowserAutomationModuleInterface

logger = get_logger("autovideofactory.browser.engine")


class PlaywrightBrowserEngine(BrowserAutomationModuleInterface):
    _playwright: Optional[Playwright] = None
    _browser: Optional[Browser] = None
    _context: Optional[BrowserContext] = None
    _page: Optional[Page] = None
    _current_url: str = ""

    def __init__(self) -> None:
        self._status = ModuleStatus.UNINITIALIZED
        self._health = ModuleHealth()

    async def initialize(self, config: Optional[dict] = None) -> None:
        self._status = ModuleStatus.INITIALIZING
        try:
            self._playwright = await async_playwright().start()
            logger.info("Playwright engine initialized")
            self._status = ModuleStatus.READY
        except Exception as e:
            self._status = ModuleStatus.ERROR
            raise BrowserError(f"Failed to initialize Playwright: {e}") from e

    async def shutdown(self) -> None:
        await self.close()
        if self._playwright:
            await self._playwright.stop()
        self._status = ModuleStatus.UNINITIALIZED
        logger.info("Playwright engine shut down")

    async def health_check(self) -> ModuleHealth:
        return ModuleHealth(
            status=self._status,
            message="Browser engine operational" if self._status == ModuleStatus.READY else "Not ready",
        )

    def get_capabilities(self):
        return [
            ModuleCapability(
                name="browser_navigation",
                description="Navigate websites and interact with pages",
                supported_providers=["playwright"],
            ),
            ModuleCapability(
                name="session_management",
                description="Save, restore, and manage browser sessions",
            ),
            ModuleCapability(
                name="vision_automation",
                description="Use screenshots and vision to interact with pages",
                supported_providers=["ocr", "openai_vision"],
            ),
        ]

    async def launch(self, headless: bool = False, profile_path: Optional[str] = None) -> bool:
        try:
            browser_type: BrowserType = getattr(self._playwright, settings.browser_type.value)

            launch_options = {
                "headless": headless or settings.browser_headless,
                "timeout": settings.browser_timeout,
            }
            if settings.browser_executable_path:
                launch_options["executable_path"] = settings.browser_executable_path

            self._browser = await browser_type.launch(**launch_options)

            context_options = {
                "viewport": {
                    "width": settings.browser_viewport_width,
                    "height": settings.browser_viewport_height,
                },
            }
            if profile_path and os.path.exists(profile_path):
                context_options["storage_state"] = profile_path

            self._context = await self._browser.new_context(**context_options)
            self._page = await self._context.new_page()

            self._page.on("pageerror", lambda err: logger.error(f"Page error: {err}"))

            self._status = ModuleStatus.RUNNING
            logger.info("Browser launched successfully")
            return True
        except Exception as e:
            raise BrowserError(f"Failed to launch browser: {e}") from e

    async def close(self) -> None:
        try:
            if self._page:
                await self._page.close()
            if self._context:
                await self._context.close()
            if self._browser:
                await self._browser.close()
        except Exception as e:
            logger.warning(f"Error closing browser: {e}")
        finally:
            self._page = None
            self._context = None
            self._browser = None
            self._status = ModuleStatus.READY

    async def navigate(self, url: str, timeout: Optional[int] = None) -> BrowserActionResult:
        self._ensure_page()
        try:
            await self._page.goto(url, wait_until="domcontentloaded", timeout=timeout or settings.browser_navigation_timeout)
            self._current_url = self._page.url
            return BrowserActionResult(success=True, data={"url": self._page.url, "title": await self._page.title()})
        except Exception as e:
            return BrowserActionResult(success=False, error=str(e))

    async def click(self, selector: str, timeout: Optional[int] = None) -> BrowserActionResult:
        self._ensure_page()
        try:
            await self._page.click(selector, timeout=timeout or settings.browser_timeout)
            return BrowserActionResult(success=True)
        except Exception as e:
            return BrowserActionResult(success=False, error=str(e))

    async def type_text(self, selector: str, text: str, delay: int = 50) -> BrowserActionResult:
        self._ensure_page()
        try:
            await self._page.fill(selector, "")
            await self._page.type(selector, text, delay=delay)
            return BrowserActionResult(success=True)
        except Exception as e:
            return BrowserActionResult(success=False, error=str(e))

    async def screenshot(self, full_page: bool = False) -> bytes:
        self._ensure_page()
        return await self._page.screenshot(full_page=full_page, type="png")

    async def get_html(self, selector: Optional[str] = None) -> str:
        self._ensure_page()
        if selector:
            element = await self._page.query_selector(selector)
            return await element.inner_html() if element else ""
        return await self._page.content()

    async def execute_script(self, script: str) -> Any:
        self._ensure_page()
        return await self._page.evaluate(script)

    async def wait_for_selector(self, selector: str, timeout: int = 30000) -> bool:
        self._ensure_page()
        try:
            await self._page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception:
            return False

    async def wait_for_navigation(self, timeout: int = 60000) -> bool:
        self._ensure_page()
        try:
            await self._page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except Exception:
            return False

    async def upload_file(self, selector: str, file_path: str) -> BrowserActionResult:
        self._ensure_page()
        try:
            file_input = await self._page.query_selector(selector)
            if not file_input:
                return BrowserActionResult(success=False, error=f"File input not found: {selector}")
            await file_input.set_input_files(file_path)
            return BrowserActionResult(success=True)
        except Exception as e:
            return BrowserActionResult(success=False, error=str(e))

    async def scroll(self, direction: str = "down", amount: int = 300) -> None:
        self._ensure_page()
        if direction == "down":
            await self._page.evaluate(f"window.scrollBy(0, {amount})")
        else:
            await self._page.evaluate(f"window.scrollBy(0, -{amount})")

    async def extract_text(self, selector: str) -> str:
        self._ensure_page()
        element = await self._page.query_selector(selector)
        if element:
            return await element.text_content() or ""
        return ""

    async def extract_links(self, selector: str = "a") -> list[dict[str, str]]:
        self._ensure_page()
        links = await self._page.evaluate(f"""
            Array.from(document.querySelectorAll('{selector}')).map(a => ({{
                href: a.href,
                text: a.textContent?.trim() || ''
            }}))
        """)
        return links

    async def get_cookies(self) -> list[dict]:
        if self._context:
            return await self._context.cookies()
        return []

    async def save_storage_state(self, path: str) -> None:
        if self._context:
            await self._context.storage_state(path=path)

    async def get_page(self) -> Page:
        self._ensure_page()
        return self._page

    def _ensure_page(self) -> None:
        if not self._page:
            raise BrowserError("Browser page not initialized. Call launch() first.")
